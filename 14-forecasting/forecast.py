#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой прогноз: скользящее среднее по месячной выручке (синтетика).
"""

from statistics import mean

# Вымышленная выручка по месяцам (млн руб.)
revenue = [10.2, 10.5, 10.1, 10.8, 11.0, 10.9, 11.2, 11.4, 11.1, 11.6, 11.5, 11.8]
window = 3

if len(revenue) < window:
    raise SystemExit("Недостаточно точек для окна")

ma_values = []
for i in range(window - 1, len(revenue)):
    ma_values.append(mean(revenue[i - window + 1 : i + 1]))

last_ma = ma_values[-1]
# Наивный шаг: следующий месяц ≈ последнее MA
forecast_next = last_ma

print("Ряд:", revenue)
print(f"MA({window}) на последней позиции: {last_ma:.2f}")
print(f"Прогноз на следующий месяц (baseline): {forecast_next:.2f}")
