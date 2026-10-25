import json
from pathlib import Path

from app.main import app

OUT = Path(__file__).resolve().parents[2] / "contracts" / "openapi.json"


def main() -> None:
    OUT.write_text(json.dumps(app.openapi(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()