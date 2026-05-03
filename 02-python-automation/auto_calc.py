#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматизация расчёта 15+ видов услуг (обезличенный рабочий сценарий ОЭЗ).
Цепочка: 1С → Excel → проверка колонок → расчёт → сводка → выходной файл.

Запуск:
  python auto_calc.py
  python auto_calc.py --input input_example.xlsx --output result.xlsx
"""

import argparse
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd

# Тарифы: учебные значения, не для продакшена
TARIFFS = {
    "cold_energy": (850.50, "kWh", "volume * rate"),
    "garbage": (45.20, "sqm", "area * rate"),
    "mop": (120.00, "sqm", "area * rate * 1.18"),
    "advertising": (500.00, "unit", "qty * rate"),
    "security": (15.00, "sqm", "area * rate"),
    "parking": (3500.00, "place", "qty * rate"),
    "customs": (15000.00, "operation", "qty * rate"),
    "congress_rent": (2500.00, "hour", "hours * rate"),
    "water": (32.10, "sqm", "area * rate"),
    "heat": (68.00, "sqm", "area * rate"),
    "hvac_service": (210.00, "unit", "qty * rate"),
    "land_rent": (420.00, "sqm", "area * rate"),
    "storage": (95.00, "sqm", "area * rate"),
    "it_infra": (1200.00, "unit", "qty * rate"),
    "cleaning_extra": (55.00, "sqm", "area * rate"),
}


def _default_input_path():
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("input_example.xlsx", "input_data.xlsx"):
        p = os.path.join(base, name)
        if os.path.isfile(p):
            return p
    return os.path.join(base, "input_example.xlsx")


def load_data(filepath):
    """Загрузка выгрузки из 1С (Excel)."""
    print(f"[+] Читаем {filepath}")
    df = pd.read_excel(filepath, sheet_name="Data")

    required = ["contract_id", "service_code", "quantity", "area", "date"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"[!] Нет колонок: {missing}")
        sys.exit(1)

    if "hours" not in df.columns:
        df["hours"] = np.nan

    return df


def calculate(row):
    """Расчёт одной строки: база зависит от формулы услуги."""
    service = row["service_code"]

    if service not in TARIFFS:
        print(f"[!] Неизвестная услуга: {service}")
        return 0.0

    rate, _unit, formula = TARIFFS[service]

    if "hours" in formula and "hour" in formula:
        base = row["hours"] if pd.notna(row["hours"]) else row["quantity"]
    elif "area" in formula:
        base = row["area"]
    elif "volume" in formula:
        base = row["quantity"]
    else:
        base = row["quantity"]

    vat = 1.18 if "1.18" in formula else 1.0
    amount = float(base) * float(rate) * vat
    return round(amount, 2)


def main():
    parser = argparse.ArgumentParser(
        description="Расчёт начислений из Excel (обезличенный пример ОЭЗ)."
    )
    parser.add_argument(
        "--input",
        default=_default_input_path(),
        help="Путь к Excel (лист Data). По умолчанию: input_example.xlsx рядом со скриптом",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Куда сохранить результат (по умолчанию result_YYYYMMDD.xlsx рядом со скриптом)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"[!] Файл не найден: {args.input}")
        print("    Положите input_example.xlsx или укажите --input явно.")
        sys.exit(1)

    out = args.output
    if not out:
        base = os.path.dirname(os.path.abspath(__file__))
        out = os.path.join(base, f"result_{datetime.now().strftime('%Y%m%d')}.xlsx")

    df = load_data(args.input)

    print(f"[+] Расчёт {len(df)} строк...")
    df["amount"] = df.apply(calculate, axis=1)

    summary = df.groupby("service_code")["amount"].sum()
    print("\n=== СВОДКА ===")
    print(summary)

    df.to_excel(out, index=False)
    print(f"\n[+] Сохранено: {out}")


if __name__ == "__main__":
    main()
