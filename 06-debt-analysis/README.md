# 06 — Дебиторка: анализ и эффект автоматизации

Ноутбук строится на **обезличенной** выгрузке из 1С (`debt_data_2022.xlsx`), агрегирует просрочку по корзинам, визуализирует **«до / после»** внедрения автоматических уведомлений и фиксирует вывод по KPI проекта.

## Связь файлов

| Файл | Роль |
|------|------|
| [debt_forecast.ipynb](debt_forecast.ipynb) | Анализ, график, вывод |
| [debt_data_2022.xlsx](debt_data_2022.xlsx) | Входные синтетические строки |
| [NOTEBOOK_OUTLINE.md](NOTEBOOK_OUTLINE.md) | Краткая логика расчётов (для ревью без запуска Jupyter) |

## Запуск

```bash
pip install pandas openpyxl numpy matplotlib
jupyter notebook debt_forecast.ipynb
```

Связь с автоматизацией расчётов: см. [02-python-automation](../02-python-automation/) — тот же паттерн работы с Excel после выгрузки из учётных систем.
