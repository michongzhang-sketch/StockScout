from __future__ import annotations

import argparse
from pathlib import Path

from stockscout.app import StockScoutApp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate stock recommendations.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Repository root containing config/ and tmp/ directories.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Optional override for the output directory.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    app = StockScoutApp(args.repo_root)
    output_path = app.run(output_dir=args.output_dir)
    print(output_path)
    return 0
