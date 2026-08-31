# Week 10 — Deployment

**Book chapters:** 10.1–10.4

Get your app online so other people can use it. This week covers deployment,
authentication, and rate limiting.

## Files

| File | What it does |
|------|-------------|
| `DEPLOY.md` | Step-by-step guides for Streamlit Cloud and Render |
| `auth_password.py` | Password gate for your Streamlit app |
| `rate_limit.py` | Simple rate limiter to prevent abuse |

## How to run

```bash
# Rate limiter demo (no API key needed)
python week-10-deployment/rate_limit.py

# Password auth demo
streamlit run week-10-deployment/auth_password.py
```

## What you should see

- `rate_limit.py` — First 3 requests allowed, then blocked, with retry-after times.
- `auth_password.py` — A password input. Enter "demo" (or set `APP_PASSWORD` env var) to see the protected content.

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Deploy fails on Streamlit Cloud | `requirements.txt` missing dependencies | Make sure all imports are in requirements.txt |
| API key not found on deploy | Secrets not configured | Add key in Streamlit Cloud secrets or Render environment variables |
| App is public and costs money | No auth or rate limiting | Add `auth_password.py` and set a billing limit |
