import json
from pathlib import Path

from app.main import app

OPENAPI = Path(__file__).resolve().parents[2] / "contracts" / "openapi.json"


def test_committed_openapi_is_up_to_date():
    committed = json.loads(OPENAPI.read_text(encoding="utf-8"))
    current = json.loads(json.dumps(app.openapi(), sort_keys=True))
    assert committed == current, (
        "contracts/openapi.json is stale. Run: cd backend && python -m scripts.export_openapi"
    )