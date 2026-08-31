"""
Support agent tools — §8.2.

Four tools the support agent can use:
  search_handbook  — look up information in the company handbook
  lookup_order     — check order status
  draft_reply      — draft a customer reply
  escalate         — flag a message for human review

AVAILABLE maps names to callables.
TOOL_SCHEMAS is the JSON the model sees.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import chromadb
from chromadb.utils import embedding_functions
from shared.client import client
from shared.chunking import chunk_text
from shared.usage import log_usage

from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-3-small"
)


# --- Handbook search (uses RAG from week 6) ---

_handbook_collection = None


def _load_handbook():
    """Load the handbook into ChromaDB once."""
    global _handbook_collection
    if _handbook_collection is not None:
        return _handbook_collection

    handbook_path = os.path.join(
        os.path.dirname(__file__), "..", "week-06-project-2-rag", "sample_docs", "handbook.txt"
    )

    if not os.path.exists(handbook_path):
        # Fallback to inline data
        return None

    with open(handbook_path, "r", encoding="utf-8") as f:
        text = f.read()

    chroma = chromadb.Client()
    try:
        chroma.delete_collection("handbook")
    except ValueError:
        pass

    _handbook_collection = chroma.create_collection(
        name="handbook", embedding_function=openai_ef
    )
    chunks = chunk_text(text)
    _handbook_collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )
    return _handbook_collection


def search_handbook(query):
    """Search the company handbook for information related to the query."""
    collection = _load_handbook()
    if collection is None:
        return "Handbook not available. Could not find handbook.txt."

    results = collection.query(query_texts=[query], n_results=2)
    chunks = results["documents"][0]
    return "\n\n".join(chunks)


# --- Order lookup ---

ORDERS = {
    "ORD-1001": {"status": "Shipped", "eta": "Thursday, Aug 28", "item": "Wireless Mouse"},
    "ORD-1002": {"status": "Processing", "eta": "Ships tomorrow", "item": "USB-C Hub"},
    "ORD-1003": {"status": "Delivered", "eta": "Delivered Aug 20", "item": "Laptop Stand"},
    "ORD-1004": {"status": "Cancelled", "eta": "N/A", "item": "Keyboard"},
    "ORD-1005": {"status": "Returned", "eta": "Refund pending", "item": "Monitor"},
}


def lookup_order(order_id):
    """Look up order status by order ID."""
    order = ORDERS.get(order_id)
    if order is None:
        return f"Order {order_id} not found in our system."
    return f"Order {order_id}: {order['item']} — {order['status']} ({order['eta']})"


# --- Draft reply ---

def draft_reply(message, tone="professional"):
    """Draft a customer reply using the model."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a customer support agent. Draft a {tone}, helpful reply to "
                    "the customer message below. Be concise. If you do not know the answer, "
                    "say you will look into it."
                ),
            },
            {"role": "user", "content": message},
        ],
        temperature=0,
    )
    log_usage(response, "gpt-4o-mini")
    return response.choices[0].message.content


# --- Escalate ---

def escalate(reason):
    """Flag a message for human review. Returns a confirmation."""
    return f"ESCALATED: This message has been flagged for human review. Reason: {reason}"


# --- AVAILABLE and TOOL_SCHEMAS ---

AVAILABLE = {
    "search_handbook": search_handbook,
    "lookup_order": lookup_order,
    "draft_reply": draft_reply,
    "escalate": escalate,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_handbook",
            "description": "Search the company handbook for policy information. Use this when a customer asks about returns, shipping, warranty, or other policies.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query, e.g. 'return policy' or 'shipping times'",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up the current status and delivery estimate for a customer order.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, formatted as 'ORD-XXXX', e.g. 'ORD-1001'",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "draft_reply",
            "description": "Draft a reply to send to the customer. Use this after gathering all needed information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Summary of the situation to base the reply on",
                    },
                    "tone": {
                        "type": "string",
                        "description": "Tone for the reply: 'professional', 'friendly', or 'empathetic'",
                        "enum": ["professional", "friendly", "empathetic"],
                    },
                },
                "required": ["message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "escalate",
            "description": "Escalate a message to a human supervisor. Use when the customer mentions legal action, safety issues, requests a supervisor, or when the issue is too complex to resolve automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Why this message needs human review",
                    }
                },
                "required": ["reason"],
            },
        },
    },
]
