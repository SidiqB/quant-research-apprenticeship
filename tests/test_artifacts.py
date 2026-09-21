"""Check durable research records, not financial performance."""

import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def test_experiment_reproduces_known_release_schedule(tmp_path):
    result_path = ROOT / "experiments/availability/results.json"
    before = result_path.read_bytes()
    subprocess.run([sys.executable, str(ROOT / "scripts/availability_experiment.py")], check=True)
    assert result_path.read_bytes() == before
    result = json.loads(before)
    assert [r["available_value"] for r in result["decisions"]] == [None, None, 100, 100, 60, 60]
    assert result["mismatched_decisions"] == 4
    assert result["data_kind"] == "synthetic"


def test_role_matrix_has_sources_and_distinct_postings():
    with (ROOT / "career_research/role_skill_matrix.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert 40 <= len(rows) <= 60
    assert len({r["url"] for r in rows}) == len(rows)
    assert len({(r["company"], r["role_title"]) for r in rows}) == len(rows)
    assert len({r["company"] for r in rows}) >= 8
    for row in rows:
        assert row["url"].startswith("https://")
        assert row["date_accessed"]
        assert row["evidence_basis"]


def renderer():
    spec = importlib.util.spec_from_file_location("render_note", ROOT / "scripts/render_note.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_report_escapes_text_and_preserves_answers(tmp_path):
    source, target = tmp_path / "note.md", tmp_path / "note.pdf"
    source.write_text("# Test note\n\nA < B & C > D.\n\n## Suggested answers\n\n42.\n")
    assert renderer().render(source, target) == 1
    text = PdfReader(target).pages[0].extract_text()
    assert "A < B & C > D." in text
    assert "Suggested answers" in text


def test_report_rejects_unsupported_glyphs(tmp_path):
    source = tmp_path / "note.md"
    source.write_text("# Test\n\n\u03b1\n")
    with pytest.raises(ValueError, match="ASCII"):
        renderer().render(source, tmp_path / "note.pdf")
