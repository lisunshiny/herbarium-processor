import sys
from .common import (
    FRONTEND_DIR,
    HOST,
    FRONTEND_PORT,
    PKG,
    hypercorn_args,
    run_processes,
)


def main():
    processes = [
        (
            hypercorn_args(),
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
