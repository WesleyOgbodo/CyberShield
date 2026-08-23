"""Stable local WSGI entry point for the Integrated Cybersecurity System."""
from pathlib import Path
import logging
import os
import sys

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)
load_dotenv(BASE_DIR / ".env")

from waitress import serve
from app import app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


def main():
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))

    print("=" * 64, flush=True)
    print("Integrated Cybersecurity System", flush=True)
    print(f"Project directory: {BASE_DIR}", flush=True)
    print(f"Listening on: http://{host}:{port}", flush=True)
    print("Keep this window open while using the application.", flush=True)
    print("Press CTRL+C to stop the server.", flush=True)
    print("=" * 64, flush=True)

    try:
        serve(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\nServer stopped by user.", flush=True)
        return 0
    except BaseException:
        logging.getLogger(__name__).exception("The WSGI server terminated unexpectedly.")
        return 1
    finally:
        print("Server process ended.", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
