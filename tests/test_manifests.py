"""Adversarial provenance checks with independent SHA-256 known-answer evidence."""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from quant_research.validation.manifests import (
    load_manifest,
    manifest_bytes,
    sha256_file,
    validate_manifest,
    verify_sources,
)

ROOT = Path(__file__).resolve().parents[1]
ABC_SHA256 = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


@pytest.fixture
def record(tmp_path):
    (tmp_path / "fixture.txt").write_bytes(b"abc")
    return {
        "schema_version": 1,
        "experiment_id": "known-answer",
        "data_kind": "synthetic",
        "question": "Do exact bytes match?",
        "hypothesis": "A one-byte change is rejected.",
        "information_period": "Undated synthetic bytes; no market period.",
        "evaluation_protocol": "Check against the SHA-256 abc known answer.",
        "sources": [{"path": "fixture.txt", "sha256": ABC_SHA256}],
    }


def test_known_answer_and_roundtrip(record, tmp_path):
    assert sha256_file(tmp_path / "fixture.txt") == ABC_SHA256
    assert verify_sources(record, tmp_path) == ("fixture.txt",)
    path = tmp_path / "manifest.json"
    path.write_bytes(manifest_bytes(record))
    assert load_manifest(path) == record
    reordered = dict(reversed(list(record.items())))
    assert manifest_bytes(reordered) == path.read_bytes()


@pytest.mark.parametrize(
    "field",
    [
        "schema_version",
        "experiment_id",
        "data_kind",
        "question",
        "hypothesis",
        "information_period",
        "evaluation_protocol",
        "sources",
    ],
)
def test_missing_fields(record, field):
    del record[field]
    with pytest.raises(ValueError):
        validate_manifest(record)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema_version", True),
        ("schema_version", 1.0),
        ("schema_version", 2),
        ("data_kind", "mixed"),
        ("data_kind", ""),
        ("question", " \t"),
        ("question", None),
        ("evaluation_protocol", []),
        ("sources", []),
        ("sources", {}),
    ],
)
def test_invalid_metadata(record, field, value):
    record[field] = value
    with pytest.raises(ValueError):
        validate_manifest(record)


@pytest.mark.parametrize("digest", [None, "", "a" * 63, "a" * 65, "g" * 64, "A" * 64])
def test_invalid_hash(record, digest):
    record["sources"][0]["sha256"] = digest
    with pytest.raises(ValueError):
        validate_manifest(record)


def test_missing_hash_and_unknown_fields(record):
    candidate = copy.deepcopy(record)
    del candidate["sources"][0]["sha256"]
    with pytest.raises(ValueError):
        validate_manifest(candidate)
    record["unexpected"] = "value"
    with pytest.raises(ValueError):
        validate_manifest(record)


@pytest.mark.parametrize(
    "path", ["", ".", "../outside", "/absolute", "a/../b", "./a", "a//b", "a\\b", "C:/a"]
)
def test_invalid_paths(record, path):
    record["sources"][0]["path"] = path
    with pytest.raises(ValueError):
        validate_manifest(record)


def test_duplicate_source(record):
    record["sources"].append(record["sources"][0].copy())
    with pytest.raises(ValueError, match="duplicate source"):
        validate_manifest(record)


@pytest.mark.parametrize(
    "content",
    [
        '{"schema_version":1,"schema_version":1}',
        '{"sources":[{"path":"a","path":"b"}]}',
    ],
)
def test_duplicate_json_keys(tmp_path, content):
    path = tmp_path / "duplicate.json"
    path.write_text(content)
    with pytest.raises(ValueError, match="duplicate JSON key"):
        load_manifest(path)


def test_changed_and_missing_file(record, tmp_path):
    path = tmp_path / "fixture.txt"
    path.write_bytes(b"abd")
    with pytest.raises(ValueError, match="checksum mismatch"):
        verify_sources(record, tmp_path)
    path.unlink()
    with pytest.raises(ValueError, match="source unavailable"):
        verify_sources(record, tmp_path)


def test_directory_and_symlink_escape(record, tmp_path):
    root = tmp_path / "root"
    root.mkdir()
    (root / "fixture.txt").mkdir()
    with pytest.raises(ValueError, match="file beneath root"):
        verify_sources(record, root)
    (root / "fixture.txt").rmdir()
    (root / "fixture.txt").symlink_to(tmp_path / "fixture.txt")
    with pytest.raises(ValueError, match="file beneath root"):
        verify_sources(record, root)


@pytest.mark.parametrize("value", [None, [], "manifest", 1])
def test_invalid_top_level(value):
    with pytest.raises(ValueError):
        validate_manifest(value)


def test_archived_sources_and_reproducible_experiment(tmp_path):
    manifest = load_manifest(ROOT / "experiments/manifests/purging-v1.json")
    assert len(verify_sources(manifest, ROOT)) == 4
    outputs = [tmp_path / "one.json", tmp_path / "two.json"]
    for output in outputs:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/manifest_experiment.py"), "--output", str(output)],
            check=True,
            capture_output=True,
            cwd=tmp_path,
        )
    assert outputs[0].read_bytes() == outputs[1].read_bytes()
    expected = ROOT / "experiments/manifests/results.json"
    assert outputs[0].read_bytes() == expected.read_bytes()
    result = json.loads(outputs[0].read_text())
    assert result["missing_metadata_rejected"] == [
        "data_kind",
        "question",
        "evaluation_protocol",
        "source_hash",
    ]
    assert result["one_byte_change_rejected"] is True
