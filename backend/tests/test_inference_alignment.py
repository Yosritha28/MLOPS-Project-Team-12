import json
from pathlib import Path

from jsonschema import Draft202012Validator

from app.schemas.inference import MatchResult

CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"


def load(name):
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


def test_example_parses_into_the_backend_model():
    MatchResult.model_validate(load("example_match_result.json"))


def test_backend_model_output_satisfies_the_inference_schema():
    model = MatchResult.model_validate(load("example_match_result.json"))
    data = model.model_dump(mode="json", exclude_none=True)
    schema = load("inference_schema.json")
    Draft202012Validator({"$ref": "#/$defs/MatchResult", "$defs": schema["$defs"]}).validate(data)