from __future__ import annotations

import json
from pathlib import Path

from stockscout.models import StockSnapshot


class ConfigDataSource:
    def __init__(self, config_path: Path) -> None:
        self._config_path = config_path

    def load(self) -> list[StockSnapshot]:
        raw_items = json.loads(self._config_path.read_text(encoding="utf-8"))
        return [StockSnapshot(**item) for item in raw_items]
