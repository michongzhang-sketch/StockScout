from __future__ import annotations

import csv
from pathlib import Path

from stockscout.models import RecommendationRow


class CsvReportWriter:
    headers = [
        "当前时间",
        "股票名",
        "股票代码",
        "当前股价",
        "股票市值",
        "推荐买入价格",
        "推荐卖出价格",
    ]

    def write(self, rows: list[RecommendationRow], output_path: Path) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(self.headers)
            for row in rows:
                writer.writerow(
                    [
                        row.current_time.isoformat(),
                        row.stock_name,
                        row.stock_code,
                        f"{row.current_price:.2f}",
                        f"{row.market_cap:.0f}",
                        f"{row.recommended_buy_price:.2f}",
                        f"{row.recommended_sell_price:.2f}",
                    ]
                )
        return output_path
