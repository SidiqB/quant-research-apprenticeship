"""Persist one uniform 0..3 draw per London date; callers hold the research run lock."""

import json
import secrets
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def get_budget(directory: Path, day: str) -> dict:
    """Reuse a day's draw, rejecting corrupt state instead of silently redrawing."""
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{day}.json"
    if not path.exists():
        result = {"date": day, "timezone": "Europe/London", "budget": secrets.randbelow(4)}
        try:
            with path.open("x") as stream:
                json.dump(result, stream)
        except FileExistsError:
            pass
    result = json.loads(path.read_text())
    if (
        result.get("date") != day
        or result.get("timezone") != "Europe/London"
        or type(result.get("budget")) is not int
        or not 0 <= result["budget"] <= 3
    ):
        raise ValueError("Invalid saved draw; investigate without redrawing")
    return result


if __name__ == "__main__":
    git_dir = Path(
        subprocess.check_output(["git", "rev-parse", "--absolute-git-dir"], text=True).strip()
    )
    day = datetime.now(ZoneInfo("Europe/London")).date().isoformat()
    print(json.dumps(get_budget(git_dir / "research-commit-budget", day), indent=2))
