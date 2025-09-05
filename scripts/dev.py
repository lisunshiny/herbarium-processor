import sys
from .common import (
    FRONTEND_DIR,
    BACKEND_APP,
    HOST,
    BACKEND_PORT,
    FRONTEND_PORT,
    PKG,
    run_processes,
)


def main():
    processes = [
        (
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
            {},
        ),
        (
            [PKG, "run", "dev", "--", "--host", HOST, "--port", FRONTEND_PORT],
            {"cwd": str(FRONTEND_DIR)},
        ),
    ]
    run_processes(processes)


if __name__ == "__main__":
    sys.exit(main())
