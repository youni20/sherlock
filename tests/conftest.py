import os
from pathlib import Path

# Make the real key available to the opt-in integration tests if a .env exists;
# otherwise fall back to a dummy so the app's Google clients can be constructed
# offline for the fast unit tests (which never actually call the API).
_env = Path(".env")
if _env.exists():
    for line in _env.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY=") and "GEMINI_API_KEY" not in os.environ:
            os.environ["GEMINI_API_KEY"] = line.split("=", 1)[1].strip()
            break

os.environ.setdefault("GEMINI_API_KEY", "test-dummy-key")
