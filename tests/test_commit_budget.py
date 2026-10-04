import importlib.util
from pathlib import Path
from unittest.mock import patch

import pytest

spec = importlib.util.spec_from_file_location(
    "budget", Path(__file__).resolve().parents[1] / "scripts/daily_commit_budget.py"
)
budget = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget)


@pytest.mark.parametrize("draw", range(4))
def test_each_value_is_saved_and_reused(tmp_path, draw):
    with patch.object(budget.secrets, "randbelow", return_value=draw) as rng:
        assert budget.get_budget(tmp_path, "2026-10-05")["budget"] == draw
        assert budget.get_budget(tmp_path, "2026-10-05")["budget"] == draw
        rng.assert_called_once_with(4)


def test_new_day_draws_again(tmp_path):
    with patch.object(budget.secrets, "randbelow", side_effect=[0, 3]):
        assert budget.get_budget(tmp_path, "2026-10-05")["budget"] == 0
        assert budget.get_budget(tmp_path, "2026-10-06")["budget"] == 3


def test_invalid_state_is_not_replaced(tmp_path):
    path = tmp_path / "2026-10-05.json"
    path.write_text('{"date":"2026-10-05","timezone":"Europe/London","budget":9}')
    with patch.object(budget.secrets, "randbelow") as rng:
        with pytest.raises(ValueError):
            budget.get_budget(tmp_path, "2026-10-05")
        rng.assert_not_called()
    assert '"budget":9' in path.read_text()
