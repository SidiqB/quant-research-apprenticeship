"""Evidence omissions and marketing claims cannot silently admit a data source."""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from quant_research.data.access import REQUIREMENTS, assess_access


def complete_record():
    return {
        "source_id": "synthetic-complete-evidence",
        "requirements": {
            name: {"status": "verified", "reference": "Synthetic evidence; no real entitlement"}
            for name in REQUIREMENTS
        },
    }


def test_complete_evidence_and_no_input_mutation():
    record = complete_record()
    before = copy.deepcopy(record)
    assessment = assess_access(record)
    assert assessment.ready
    assert assessment.blockers == ()
    assert record == before


@pytest.mark.parametrize("name", REQUIREMENTS)
@pytest.mark.parametrize("status", ["unknown", "documented", "failed"])
def test_every_unverified_requirement_blocks(name, status):
    record = complete_record()
    record["requirements"][name]["status"] = status
    result = assess_access(record)
    assert not result.ready
    assert result.blockers == (name,)


@pytest.mark.parametrize("name", REQUIREMENTS)
def test_missing_requirement_is_invalid(name):
    record = complete_record()
    del record["requirements"][name]
    with pytest.raises(ValueError, match="eight required gates"):
        assess_access(record)


@pytest.mark.parametrize("status", [True, None, [], "Verified", "", "approved"])
def test_bad_status_is_invalid(status):
    record = complete_record()
    record["requirements"]["local_access"]["status"] = status
    with pytest.raises(ValueError, match="invalid status"):
        assess_access(record)


@pytest.mark.parametrize("reference", [None, 42, "", "  "])
def test_empty_or_nontext_evidence_is_invalid(reference):
    record = complete_record()
    record["requirements"]["licence_entitlement"]["reference"] = reference
    with pytest.raises(ValueError, match="evidence reference"):
        assess_access(record)


@pytest.mark.parametrize("source_id", [None, 42, "", " "])
def test_invalid_source_identifier(source_id):
    record = complete_record()
    record["source_id"] = source_id
    with pytest.raises(ValueError, match="source_id"):
        assess_access(record)


def test_malformed_and_unknown_fields_are_rejected():
    for record in (None, [], {}, {**complete_record(), "ready": True}):
        with pytest.raises(ValueError):
            assess_access(record)
    record = complete_record()
    record["requirements"]["unexpected"] = {"status": "verified", "reference": "test"}
    with pytest.raises(ValueError):
        assess_access(record)
    for item in (
        None,
        {},
        {"status": "verified"},
        {"status": "verified", "reference": "x", "x": 1},
    ):
        record = complete_record()
        record["requirements"]["terminal_events"] = item
        with pytest.raises(ValueError):
            assess_access(record)


def test_blocker_order_is_independent_of_input_order():
    record = complete_record()
    record["requirements"] = dict(reversed(list(record["requirements"].items())))
    for evidence in record["requirements"].values():
        evidence["status"] = "unknown"
    assert assess_access(record).blockers == REQUIREMENTS


def test_experiment_reproduces_independent_expected_results(tmp_path):
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "result.json"
    subprocess.run(
        [sys.executable, str(root / "scripts/access_experiment.py"), "--output", str(output)],
        check=True,
    )
    result = json.loads(output.read_text())
    assert result["synthetic_gate_checks"] == {"complete_passes": True, "downgrades_blocked": 24}
    assert result["synthetic_survivorship_example"] == {
        "period": "one invented holding period",
        "full_population_return": -0.3,
        "survivors_only_return": 0.05,
        "difference_percentage_points": 35.0,
    }
    assert [x["source_id"] for x in result["candidate_assessments"]] == [
        "crsp-us-stock",
        "norgate-us-platinum",
    ]
    assert all(not x["ready"] for x in result["candidate_assessments"])
    assert output.read_bytes() == (root / "experiments/data_access/results.json").read_bytes()
