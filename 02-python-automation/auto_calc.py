#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Автоматизация расчёта 15+ видов услуг
Исходные данные из 1С → Excel → проверка → выгрузка

Запуск: python auto_calc.py --input data.xlsx --output result.xlsx
"""

import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import sys

# TODO: добавить логирование в файл, пока print
# TODO: обработка ошибок — криво, надо try-except нормально

TARIFFS = {
    # вид услуги: (тариф, единица, формула)
    'cold_energy': (850.50, 'kWh', 'volume * rate'),
    'garbage': (45.20, 'sqm', 'area * rate'),
    'mop': (120.00, 'sqm', 'area * rate * 1.18'),  # НДС
    'advertising': (500.00, 'unit', 'qty * rate'),
    'security': (15.00, 'sqm', 'area * rate'),
    'parking': (3500.00, 'place', 'qty * rate'),
    'customs': (15000.00, 'operation', 'qty * rate'),
    'congress_rent': (2500.00, 'hour', 'hours * rate'),
    # ... остальные 7 TODO: дописать
}

def load_data(filepath):
    """Загрузка из 1С (выгрузка в Excel)"""
    print(f"[+] Читаем {filepath}")
    df = pd.read_excel(filepath, sheet_name='Data')
    
    # проверка колонок
    required = ['contract_id', 'service_code', 'quantity', 'area', 'date']
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"[!] Нет колонок: {missing}")
        sys.exit(1)
    
    return df

def calculate(row):
    """Расчёт строки"""
    service = row['service_code']
    
    if service not in TARIFFS:
        print(f"[!] Неизвестная услуга: {service}")
        return 0  # костыль — лучше raise Exception
    
    rate, unit, formula = TARIFFS[service]
    
    # парсим формулу (упрощённо)
    if 'area' in formula:
        base = row['area']
    elif 'volume' in formula:
        base = row['quantity']  # TODO: разделить volume и quantity
    else:
        base = row['quantity']
    
    # коэффициенты
    vat = 1.18 if '1.18' in formula else 1.0
    
    amount = base * rate * vat
    
    return round(amount, 2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default=f"result_{datetime.now().strftime('%Y%m%d')}.xlsx")
    args = parser.parse_args()
    
    df = load_data(args.input)
    
    print(f"[+] Расчёт {len(df)} строк...")
    df['amount'] = df.apply(calculate, axis=1)
    
    # сводка
    summary = df.groupby('service_code')['amount'].sum()
    print("\n=== СВОДКА ===")
    print(summary)
    
    # сохраняем
    df.to_excel(args.output, index=False)
    print(f"\n[+] Сохранено: {args.output}")
    
    # TODO: добавить отправку на email бухгалтерии

if __name__ == '__main__':
    main()