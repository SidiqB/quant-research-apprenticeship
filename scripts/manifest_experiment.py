"""Audit an archived synthetic Q002 record; demonstrate stale-source rejection."""

import argparse
import copy
import json
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from quant_research.validation.manifests import load_manifest, validate_manifest, verify_sources

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "experiments/manifests/results.json")
    args = parser.parse_args()
    manifest = load_manifest(ROOT / "experiments/manifests/purging-v1.json")
    verified = verify_sources(manifest, ROOT)
    rejected = []
    for field in ("data_kind", "question", "evaluation_protocol", "source_hash"):
        candidate = copy.deepcopy(manifest)
        if field == "source_hash":
            del candidate["sources"][0]["sha256"]
        else:
            del candidate[field]
        try:
            validate_manifest(candidate)
        except ValueError:
            rejected.append(field)
        else:
            raise AssertionError(f"Missing {field} was accepted")
    with TemporaryDirectory() as directory:
        root = Path(directory)
        for name in verified:
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, destination)
        verify_sources(manifest, root)
        changed = root / "experiments/purging/results.json"
        with changed.open("ab") as stream:
            stream.write(b" ")
        try:
            verify_sources(manifest, root)
        except ValueError as exc:
            if "checksum mismatch" not in str(exc):
                raise
        else:
            raise AssertionError("Changed source was accepted")
    result = {
        "data_kind": "synthetic",
        "verified_source_count": len(verified),
        "missing_metadata_rejected": rejected,
        "one_byte_change_rejected": True,
        "interpretation": (
            "Byte integrity and metadata checks only; no empirical or authenticity claim."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
