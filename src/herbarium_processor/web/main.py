from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from herbarium_processor.config import TMP_DIR

from .routers import batches

app = FastAPI(title="Herbarium Processor Web")

STATIC_DIR = Path(__file__).parent / "static"
FRONTEND_DIST = (
    STATIC_DIR / "frontend" / "dist"
)  # e.g., Docker copies Vite dist -> this path

# Routers
app.include_router(batches.router, prefix="/api")


@app.middleware("http")
async def redirect_www_to_apex(request: Request, call_next):
    host = request.headers.get("host", "")
    if host.startswith("www."):
        url = request.url.replace(netloc=host[4:])
        return RedirectResponse(str(url), status_code=301)
    return await call_next(request)


@app.get("/healthz")
async def healthz():
    return {"ok": True}


if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
else:
    # Helpful local fallback if you run the server without building the frontend
    @app.get("/")
    async def _no_frontend():
        return PlainTextResponse(
            "Frontend build not found. Run `npm run build` and ensure dist/ is copied to "
            f"{FRONTEND_DIST}",
            status_code=503,
        )
