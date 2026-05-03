# 02 — Автоматизация расчётов (Python, обезличено)

Скрипт воспроизводит рабочий контур **«1С → Excel-выгрузка → проверка колонок → расчёт 15+ услуг → сводка → файл результата»**. Названия резидентов и договоров — **фейковые**; тарифы — **учебные**, не совпадают с действующими прейскурантами.

## Связь файлов

| Файл | Роль |
|------|------|
| [auto_calc.py](auto_calc.py) | Основной скрипт расчёта |
| [validate_input.py](validate_input.py) | Проверка колонок и дубликатов до прогона |
| [input_example.xlsx](input_example.xlsx) | **Готовый пример** для запуска «из коробки» (лист `Data`) |
| [input_data.xlsx](input_data.xlsx) | Альтернативный короткий пример |
| [RUNBOOK.md](RUNBOOK.md) | Как прогонять у себя и что проверить вручную |

## Быстрый старт

```bash
pip install pandas openpyxl numpy
cd 02-python-automation
python auto_calc.py
```

По умолчанию читается `input_example.xlsx`, результат — `result_YYYYMMDD.xlsx` в текущей папке.

```bash
python auto_calc.py --input input_data.xlsx --output my_result.xlsx
```

Связь с SQL-контуром тарифов: см. [01-sql-tariffs](../01-sql-tariffs/) — там же логика справочников и периодов.
