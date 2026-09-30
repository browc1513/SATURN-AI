"""Run a read-only import check: python -m data_analysis SHOT.CSV ..."""

import argparse
import json

from data_analysis.sl1000 import inspect_sl1000


def main():
    parser = argparse.ArgumentParser(description="Inspect SL1000 shot files without modifying them")
    parser.add_argument("paths", nargs="+", help="CSV files to inspect")
    args = parser.parse_args()
    print(json.dumps([inspect_sl1000(path).to_dict() for path in args.paths], indent=2))


if __name__ == "__main__":
    main()
