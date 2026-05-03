#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Очистка и валидация табличных данных (демо на синтетике).
"""

import re
from datetime import datetime
from typing import Optional

import pandas as pd


def normalize_phone(value: str) -> Optional[str]:
    if pd.isna(value) or value == "":
        return None
    digits = re.sub(r"\D+", "", str(value))
    if len(digits) == 10:
        return "+7" + digits
    if len(digits) == 11 and digits.startswith("8"):
        return "+7" + digits[1:]
    if len(digits) == 11 and digits.startswith("7"):
        return "+" + digits
    return None


def parse_date(value) -> Optional[datetime]:
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(str(value).strip(), fmt)
        except ValueError:
            continue
    return None


def main():
    raw = pd.DataFrame(
        {
            "id": [1, 2, 2, 3],
            "phone": ["8 (999) 000-00-01", "+79990000002", "+7 999 000 00 02", "abc"],
            "signed_at": ["01.05.2024", "2024-05-02", "2024-05-02", ""],
            "amount": [100.0, 200.5, 200.5, -1.0],
        }
    )

    print("Исходные строки:", len(raw))
    df = raw.drop_duplicates(subset=["id", "phone", "signed_at"], keep="first")
    df["phone_norm"] = df["phone"].map(normalize_phone)
    df["signed_at_parsed"] = df["signed_at"].map(parse_date)
    df["amount_ok"] = df["amount"] >= 0

    bad_phones = df["phone_norm"].isna().sum()
    bad_dates = df["signed_at_parsed"].isna().sum()
    bad_amounts = (~df["amount_ok"]).sum()

    print("\n=== Отчёт качества ===")
    print(f"Строк после дедупликации: {len(df)}")
    print(f"Телефоны не распознаны: {bad_phones}")
    print(f"Даты не распознаны: {bad_dates}")
    print(f"Суммы < 0: {bad_amounts}")
    print("\n=== Результат ===")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
