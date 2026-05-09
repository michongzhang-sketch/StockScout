from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


def build_timestamped_output_path(output_dir: Path, now: datetime | None = None) -> Path:
    current = now or datetime.now(timezone.utc)
    timestamp = current.strftime("%Y%m%dT%H%M%S%fZ")
    return output_dir / f"stock_recommendations_{timestamp}.csv"
