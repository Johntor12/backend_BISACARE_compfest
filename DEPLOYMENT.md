# Deployment (Vercel)

Minimal setup to deploy this FastAPI backend to Vercel serverless.

## Files Added

- `vercel.json`: Configures a single Python serverless function that routes all paths to FastAPI.
- `api/index.py`: Vercel entrypoint that imports the `app` from `main.py`.

## Assumptions

- Using async SQLAlchemy + `databases` with a remote Postgres (Neon / Supabase / Railway, etc.).
- `DATABASE_URL` is provided as a Vercel Environment Variable (PostgreSQL async URL, e.g. `postgresql+asyncpg://user:pass@host/dbname`).

## Environment Variables (Vercel)

Set these in Project Settings > Environment Variables:

- `DATABASE_URL`
- Any auth/token secrets you introduce later (e.g. `JWT_SECRET`, etc.)

## Deployment Steps

1. Push the branch to GitHub.
2. Create a new Vercel Project, import this repo.
3. Framework Preset: Choose "Other" (Vercel will detect Python).
4. Root directory: `/` (leave empty).
5. Build & Output Settings: leave defaults (no build command needed).
6. Add environment variables.
7. Deploy.

## Testing Locally (Optional)

You can emulate most behavior locally with uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

## Notes

- Cold starts: First request after idle may be slower.
- Long-lived DB connections: The lifespan event creates a connection on each invocation container. Vercel may freeze containers; ensure your Postgres provider tolerates abrupt disconnects. If issues arise, move to per-request connection handling.
- WebSockets: Vercel serverless Python does NOT support WebSockets; if you rely on them, consider moving to a persistent host (Railway, Fly.io, Render) or Vercel Edge Functions with a different stack.

## Adjusting for Serverless

If connection pooling becomes an issue, refactor to create an engine lazily and dispose it during shutdown:

```python
# Example idea (not yet applied)
from sqlalchemy.ext.asyncio import create_async_engine
engine = None
async def get_engine():
    global engine
    if engine is None:
        engine = create_async_engine(DATABASE_URL, echo=False)
    return engine
```

## Troubleshooting

- 500 on all routes: Verify `DATABASE_URL` is the async form.
- Module not found: Ensure `main.py` stays at repository root.
- Migration handling: Alembic migrations aren't auto-run in serverless. Run them manually from a dev machine or CI against the remote DB before deploy.

---

This is a minimal configuration; expand as needed (logging, metrics, auth secrets, migrations workflow).
