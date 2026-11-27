"""Writes the OpenAPI schema to api/openapi.json (input for the generated web client)."""

import json
from pathlib import Path

from app.main import create_app

OUTPUT = Path(__file__).resolve().parent.parent / "openapi.json"


def main() -> None:
    schema = create_app().openapi()
    OUTPUT.write_text(json.dumps(schema, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
