"""Versioned experiment records and byte-level provenance checks, not authenticity."""

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import cast

_FIELDS = {
    "schema_version",
    "experiment_id",
    "data_kind",
    "question",
    "hypothesis",
    "information_period",
    "evaluation_protocol",
    "sources",
}
_TEXT_FIELDS = _FIELDS - {"schema_version", "sources"}


def sha256_file(path: Path) -> str:
    """Hash exact file bytes, including whitespace and line endings."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def validate_manifest(value: object) -> dict[str, object]:
    """Accept only schema v1; reject omissions, unknown fields and ambiguous paths."""
    if not isinstance(value, dict) or set(value) != _FIELDS:
        raise ValueError("manifest must contain exactly the schema v1 fields")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise ValueError("unsupported schema_version; expected integer 1")
    for field in _TEXT_FIELDS:
        if not isinstance(value[field], str) or not value[field].strip():
            raise ValueError(f"{field} must be nonblank text")
    if value["data_kind"] not in {"synthetic", "real"}:
        raise ValueError("data_kind must be synthetic or real")
    sources = value["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources must be a nonempty list")
    seen = set()
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"path", "sha256"}:
            raise ValueError("each source requires exactly path and sha256")
        path, digest = source["path"], source["sha256"]
        if not isinstance(path, str) or not path.strip():
            raise ValueError("source path must be nonblank text")
        parsed = PurePosixPath(path)
        if (
            parsed.is_absolute()
            or ".." in parsed.parts
            or "\\" in path
            or ":" in path
            or str(parsed) != path
            or path == "."
        ):
            raise ValueError("source path must be a normalized relative POSIX path")
        if path in seen:
            raise ValueError("duplicate source path")
        seen.add(path)
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("source sha256 must be 64 lowercase hexadecimal characters")
    return cast(dict[str, object], value)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_manifest(path: Path) -> dict[str, object]:
    """Parse UTF-8 JSON, rejecting duplicate keys even in nested source records."""
    return validate_manifest(
        json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object)
    )


def manifest_bytes(value: object) -> bytes:
    """Stable project serialization; list order matters. Not a universal JSON standard."""
    validated = validate_manifest(value)
    return (json.dumps(validated, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode(
        "utf-8"
    )


def verify_sources(value: object, root: Path) -> tuple[str, ...]:
    """Verify all declared files beneath root; raise on absent/changed/escaping files.

    Files must be quiescent during verification. This is not a hostile-filesystem sandbox.
    Metadata validity alone never establishes the presence or contents of source files.
    """
    manifest = validate_manifest(value)
    root = root.resolve(strict=True)
    sources = cast(list[dict[str, str]], manifest["sources"])
    verified = []
    for source in sources:
        try:
            path = (root / source["path"]).resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise ValueError(f"source unavailable: {source['path']}") from exc
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError(f"source must be a file beneath root: {source['path']}")
        if sha256_file(path) != source["sha256"]:
            raise ValueError(f"source checksum mismatch: {source['path']}")
        verified.append(source["path"])
    return tuple(verified)
