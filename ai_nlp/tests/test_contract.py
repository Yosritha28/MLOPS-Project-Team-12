import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

CONTRACTS = Path(__file__).resolve().parents[2] / "contracts"


def load(name):
    return json.loads((CONTRACTS / name).read_text(encoding="utf-8"))


def validator_for(def_name):
    schema = load("inference_schema.json")
    return Draft202012Validator({"$ref": f"#/$defs/{def_name}", "$defs": schema["$defs"]})


@pytest.mark.parametrize(
    "example, def_name",
    [
        ("example_parsed_resume.json", "ParsedResume"),
        ("example_parsed_job.json", "ParsedJob"),
        ("example_match_result.json", "MatchResult"),
    ],
)
def test_example_matches_schema(example, def_name):
    validator_for(def_name).validate(load(example))


def test_bad_score_is_rejected():
    bad = load("example_match_result.json")
    bad["overall_score"] = 150
    assert not validator_for("MatchResult").is_valid(bad)


def test_missing_field_is_rejected():
    bad = load("example_match_result.json")
    del bad["model_version"]
    assert not validator_for("MatchResult").is_valid(bad)



def test_extras_are_accepted():
    ok = load("example_match_result.json")
    ok["extras"] = {"anything": "goes here", "n": 1}
    assert validator_for("MatchResult").is_valid(ok)


def test_unknown_top_level_field_is_rejected():
    bad = load("example_match_result.json")
    bad["surprise"] = 1
    assert not validator_for("MatchResult").is_valid(bad)


def test_missing_schema_version_is_rejected():
    bad = load("example_match_result.json")
    del bad["schema_version"]
    assert not validator_for("MatchResult").is_valid(bad)


def test_bad_schema_version_is_rejected():
    bad = load("example_match_result.json")
    bad["schema_version"] = "v1"
    assert not validator_for("MatchResult").is_valid(bad)