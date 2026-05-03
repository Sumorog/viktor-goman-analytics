#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Проверка Excel перед массовым расчётом (обезличенный вспомогательный скрипт)."""
import argparse
import os
import sys

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=os.path.join(os.path.dirname(__file__), "input_example.xlsx"),
    )
    args = parser.parse_args()
    if not os.path.isfile(args.input):
        print("[!] Нет файла:", args.input)
        sys.exit(1)
    df = pd.read_excel(args.input, sheet_name="Data")
    required = ["contract_id", "service_code", "quantity", "area", "date"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print("[!] Нет колонок:", missing)
        sys.exit(2)
    dup = df.duplicated(subset=["contract_id", "service_code", "date"]).sum()
    print("[+] OK, строк:", len(df), "| дубликатов по ключу:", int(dup))
    sys.exit(0 if dup == 0 else 3)


if __name__ == "__main__":
    main()
