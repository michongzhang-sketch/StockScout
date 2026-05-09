from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP


BUY_DISCOUNT = Decimal("0.97")
SELL_PREMIUM = Decimal("1.10")
TWOPLACES = Decimal("0.01")


def _to_money(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class StockAnalysis:
    symbol: str
    current_date: date
    current_price: Decimal
    suggested_buy_price: Decimal
    suggested_sell_price: Decimal


def analyze_stock_selection(symbol: str, current_price: Decimal, analysis_date: date | None = None) -> StockAnalysis:
    if current_price <= 0:
        raise ValueError("Current price must be greater than 0.")

    normalized_symbol = symbol.strip().upper()
    if not normalized_symbol:
        raise ValueError("Symbol is required.")

    selected_date = analysis_date or date.today()
    normalized_price = _to_money(current_price)

    return StockAnalysis(
        symbol=normalized_symbol,
        current_date=selected_date,
        current_price=normalized_price,
        suggested_buy_price=_to_money(normalized_price * BUY_DISCOUNT),
        suggested_sell_price=_to_money(normalized_price * SELL_PREMIUM),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="分析选择的股票并给出买卖价格建议。")
    parser.add_argument("--symbol", required=True, help="股票代码，例如 AAPL")
    parser.add_argument("--price", required=True, type=Decimal, help="当前价格")
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    result = analyze_stock_selection(args.symbol, args.price)

    print(f"股票代码: {result.symbol}")
    print(f"当前日期: {result.current_date.isoformat()}")
    print(f"当前价格: {result.current_price:.2f}")
    print(f"建议买入价格: {result.suggested_buy_price:.2f}")
    print(f"建议卖出价格: {result.suggested_sell_price:.2f}")


if __name__ == "__main__":
    main()
