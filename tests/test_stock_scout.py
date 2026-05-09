from datetime import date
from decimal import Decimal
import unittest

from stock_scout import analyze_stock_selection


class AnalyzeStockSelectionTests(unittest.TestCase):
    def test_returns_expected_fields(self) -> None:
        result = analyze_stock_selection("aapl", Decimal("150"), analysis_date=date(2026, 5, 9))

        self.assertEqual(result.symbol, "AAPL")
        self.assertEqual(result.current_date, date(2026, 5, 9))
        self.assertEqual(result.current_price, Decimal("150.00"))
        self.assertEqual(result.suggested_buy_price, Decimal("145.50"))
        self.assertEqual(result.suggested_sell_price, Decimal("165.00"))

    def test_rejects_non_positive_price(self) -> None:
        with self.assertRaises(ValueError):
            analyze_stock_selection("AAPL", Decimal("0"))

        with self.assertRaises(ValueError):
            analyze_stock_selection("AAPL", Decimal("-1"))

    def test_rejects_blank_symbol(self) -> None:
        with self.assertRaises(ValueError):
            analyze_stock_selection("   ", Decimal("100"))


if __name__ == "__main__":
    unittest.main()
