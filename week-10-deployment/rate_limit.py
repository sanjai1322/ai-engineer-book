"""
Rate limiting — Chapter 10.

Simple in-memory rate limiter that tracks requests per user session.
Prevents a single user from making too many API calls too quickly.
"""

import sys
import os
import time
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class RateLimiter:
    """Simple rate limiter: max_requests per window_seconds."""

    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, user_id="default"):
        """Check if a request is allowed for the given user."""
        now = time.time()
        window_start = now - self.window_seconds

        # Remove old requests outside the window
        self.requests[user_id] = [
            t for t in self.requests[user_id] if t > window_start
        ]

        if len(self.requests[user_id]) >= self.max_requests:
            return False

        self.requests[user_id].append(now)
        return True

    def remaining(self, user_id="default"):
        """How many requests are left in the current window."""
        now = time.time()
        window_start = now - self.window_seconds

        recent = [t for t in self.requests[user_id] if t > window_start]
        return max(0, self.max_requests - len(recent))

    def retry_after(self, user_id="default"):
        """Seconds until the next request will be allowed."""
        if not self.requests[user_id]:
            return 0

        now = time.time()
        oldest = min(self.requests[user_id])
        wait = (oldest + self.window_seconds) - now
        return max(0, wait)


def main():
    # Demo: 3 requests per 5 seconds
    limiter = RateLimiter(max_requests=3, window_seconds=5)

    print("Rate Limiter Demo")
    print(f"  Max requests: {limiter.max_requests}")
    print(f"  Window: {limiter.window_seconds} seconds\n")

    for i in range(6):
        allowed = limiter.is_allowed("user-1")
        remaining = limiter.remaining("user-1")

        if allowed:
            print(f"  Request {i + 1}: ALLOWED ({remaining} remaining)")
        else:
            retry = limiter.retry_after("user-1")
            print(f"  Request {i + 1}: BLOCKED (retry after {retry:.1f}s)")

        time.sleep(1)


if __name__ == "__main__":
    main()
