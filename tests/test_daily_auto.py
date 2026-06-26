"""Tests for scripts/daily-auto.py — next_rotation and rotation logic."""

import importlib.util
import json
import sys
from pathlib import Path
from unittest.mock import mock_open, patch

# Cargar daily-auto.py como módulo (tiene guión, no se puede import normal)
DAILY_AUTO_PATH = Path(__file__).resolve().parent.parent / "scripts" / "daily-auto.py"
spec = importlib.util.spec_from_file_location("daily_auto_mod", DAILY_AUTO_PATH)
daily_auto = importlib.util.module_from_spec(spec)
sys.modules["daily_auto_mod"] = daily_auto
spec.loader.exec_module(daily_auto)

next_rotation = daily_auto.next_rotation
ROTATIONS = daily_auto.ROTATIONS


def test_next_rotation_no_state_file():
    """Sin archivo de estado, arranca en índice 0."""
    with patch.object(Path, "exists", return_value=False), \
         patch("builtins.open", mock_open()) as m:
        result = next_rotation()
    assert result == ROTATIONS[0]
    # Verifica que escribió el estado con idx=0
    handle = m()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    state = json.loads(written)
    assert state["idx"] == 0


def test_next_rotation_from_index_2():
    """Con estado existente en índice 2, devuelve el 3."""
    mock_state = json.dumps({"idx": 2, "date": "2026-06-25"})
    with patch.object(Path, "exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=mock_state)) as m:
        result = next_rotation()
    assert result == ROTATIONS[3]
    # Verifica que persistió idx=3
    handle = m()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    state = json.loads(written)
    assert state["idx"] == 3


def test_next_rotation_wrap_around():
    """Con estado en el último índice, vuelve al 0 (wrap-around)."""
    last_idx = len(ROTATIONS) - 1
    mock_state = json.dumps({"idx": last_idx, "date": "2026-06-25"})
    with patch.object(Path, "exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=mock_state)) as m:
        result = next_rotation()
    assert result == ROTATIONS[0]
    handle = m()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    state = json.loads(written)
    assert state["idx"] == 0


def test_next_rotation_corrupt_state():
    """Si el archivo de estado está corrupto, arranca en 0."""
    with patch.object(Path, "exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="not-json{broken")) as m:
        result = next_rotation()
    assert result == ROTATIONS[0]
    handle = m()
    written = "".join(call.args[0] for call in handle.write.call_args_list)
    state = json.loads(written)
    assert state["idx"] == 0
