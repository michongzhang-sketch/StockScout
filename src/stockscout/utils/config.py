from __future__ import annotations

import json
from pathlib import Path

from stockscout.models import StrategyConfig


def load_strategy_config(config_path: Path) -> StrategyConfig:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    return StrategyConfig(**raw)
