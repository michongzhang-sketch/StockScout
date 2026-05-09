from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from stockscout.app import StockScoutApp


class StockScoutAppTests(unittest.TestCase):
    def test_generates_timestamped_csv_report(self) -> None:
        runtime = datetime(2026, 5, 9, 11, 34, 6, 908000, tzinfo=timezone.utc)
        with TemporaryDirectory() as temp_dir:
            app = StockScoutApp(REPO_ROOT)
            output_path = app.run(now=runtime, output_dir=Path(temp_dir))

            self.assertEqual(output_path.name, "stock_recommendations_20260509T113406908000Z.csv")
            self.assertTrue(output_path.exists())

            with output_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.reader(handle))

        self.assertEqual(
            rows[0],
            ["当前时间", "股票名", "股票代码", "当前股价", "股票市值", "推荐买入价格", "推荐卖出价格"],
        )
        self.assertGreaterEqual(len(rows), 2)
        self.assertEqual(rows[1][0], runtime.isoformat())
        self.assertEqual(rows[1][1], "Johnson & Johnson")
        self.assertEqual(rows[1][2], "JNJ")

    def test_filters_high_risk_stocks(self) -> None:
        app = StockScoutApp(REPO_ROOT)
        output_path = app.run(now=datetime.now(timezone.utc), output_dir=REPO_ROOT / "tmp")
        with output_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        symbols = {row["股票代码"] for row in rows}
        self.assertNotIn("TSLA", symbols)
        output_path.unlink()

    def test_cli_uses_repository_root_by_default(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "stockscout", "--output-dir", str(REPO_ROOT / "tmp")],
            cwd=REPO_ROOT,
            env={"PYTHONPATH": str(SRC_ROOT)},
            check=True,
            capture_output=True,
            text=True,
        )
        output_path = Path(result.stdout.strip())
        self.assertTrue(output_path.exists())
        output_path.unlink()


if __name__ == "__main__":
    unittest.main()
