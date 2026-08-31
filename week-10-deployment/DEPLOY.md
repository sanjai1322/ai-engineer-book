# Deploying Your AI App

Step-by-step guides for getting your app online. Pick whichever platform
you prefer — both have free tiers that work for a portfolio project.

---

## Option 1: Streamlit Cloud (easiest)

Streamlit Cloud deploys directly from your GitHub repo. No server
configuration needed.

### Steps

1. **Push your code to GitHub** (see the root README for the git sequence)

2. **Go to [share.streamlit.io](https://share.streamlit.io)** and sign in
   with your GitHub account

3. **Click "New app"** and select your repo, branch, and the path to your
   Streamlit file (e.g. `week-06-project-2-rag/app.py`)

4. **Add your secrets** — click "Advanced settings" before deploying:
   ```toml
   # .streamlit/secrets.toml format
   OPENAI_API_KEY = "your-key-here"
   ```
   Streamlit Cloud reads these as environment variables. Never put keys in
   your code or repo.

5. **Click Deploy** — your app will be live in about 2 minutes at a URL like
   `https://your-app-name.streamlit.app`

### Updating

Push to your main branch. Streamlit Cloud redeploys automatically.

### Limits

- Free tier: 1 app, limited resources
- Apps sleep after inactivity; first visit after sleep takes a few seconds
- 1 GB memory limit

---

## Option 2: Render (more control)

Render gives you a proper web server. Better for apps that need background
processing or more resources.

### Steps

1. **Create a `render.yaml`** in your repo root (or just use the dashboard):
   ```yaml
   services:
     - type: web
       name: ai-engineer-app
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: streamlit run week-06-project-2-rag/app.py --server.port $PORT --server.address 0.0.0.0
   ```

2. **Go to [render.com](https://render.com)** and sign in with GitHub

3. **Click "New +"** → "Web Service" and connect your repo

4. **Set environment variables** in the Render dashboard:
   - Key: `OPENAI_API_KEY`
   - Value: your API key

5. **Deploy** — Render builds and starts your app. You get a URL like
   `https://ai-engineer-app.onrender.com`

### Updating

Push to your main branch. Render rebuilds automatically.

### Limits

- Free tier: services spin down after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 512 MB memory on free tier

---

## Before you deploy — checklist

- [ ] API key is in environment variables, not in code
- [ ] `.env` is in `.gitignore`
- [ ] Run `git log --all -p | grep -i "sk-"` to check for leaked keys in history
- [ ] Test locally with a fresh `pip install` to make sure `requirements.txt` is complete
- [ ] Add basic auth if the app should not be public (see `auth_password.py`)

---

## Cost warning

Your deployed app will use your OpenAI API key for every visitor's request.
Set a spending limit at https://platform.openai.com/account/billing to avoid
surprises. For a portfolio demo, $5-10/month is usually enough.
