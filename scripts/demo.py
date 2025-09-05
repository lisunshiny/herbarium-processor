import subprocess
import sys
from .common import (
    FRONTEND_DIR,
    BACKEND_APP,
    HOST,
    BACKEND_PORT,
    PKG,
    get_env,
    run_processes,
)


def main():
    env = get_env()
    subprocess.run([PKG, "run", "build"], cwd=str(FRONTEND_DIR), env=env, check=True)
    backend_cmd = [
        "poetry",
        "run",
        "uvicorn",
        BACKEND_APP,
        "--host",
        HOST,
        "--port",
        BACKEND_PORT,
        "--workers",
        "8",
    ]
    run_processes([(backend_cmd, {})], env=env)


if __name__ == "__main__":
    sys.exit(main())
