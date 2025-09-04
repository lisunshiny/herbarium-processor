import os
import signal
import subprocess
import sys
import time
from pathlib import Path

# --- Config ---
ROOT = Path(__file__).resolve().parents[1]  # repo root
FRONTEND_DIR = ROOT / "src" / "herbarium_processor" / "web" / "frontend"
BACKEND_APP = "herbarium_processor.web.main:app"  # uvicorn import path
HOST = os.environ.get("HOST", "0.0.0.0")
BACKEND_PORT = os.environ.get("BACKEND_PORT", "8000")
FRONTEND_PORT = os.environ.get("FRONTEND_PORT", "5173")
PKG = os.environ.get("PKG", "npm")  # or pnpm/yarn


def main():
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")

    procs = []
    try:
        # Backend (FastAPI)
        procs.append(
            subprocess.Popen(
                [
                    "poetry",
                    "run",
                    "uvicorn",
                    BACKEND_APP,
                    "--reload",
                    "--host",
                    HOST,
                    "--port",
                    BACKEND_PORT,
                ],
                env=env,
            )
        )

        # Frontend (Vite)
        procs.append(
            subprocess.Popen(
                [PKG, "run", "dev", "--", "--host", HOST, "--port", FRONTEND_PORT],
                cwd=str(FRONTEND_DIR),
                env=env,
            )
        )

        # Wait on children; exit if either dies
        while True:
            time.sleep(0.5)
            for p in procs:
                if p.poll() is not None:
                    raise KeyboardInterrupt

    except KeyboardInterrupt:
        pass
    finally:
        for p in procs:
            if p.poll() is None:
                try:
                    p.send_signal(signal.SIGINT)
                except Exception:
                    pass
        for p in procs:
            try:
                p.wait(timeout=5)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass


if __name__ == "__main__":
    sys.exit(main())
