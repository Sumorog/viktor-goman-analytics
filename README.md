# Аналитика: от тарифов до ИИ

[![SQL](https://img.shields.io/badge/SQL-3%20примера-blue)](01-sql-tariffs/)
[![Python](https://img.shields.io/badge/Python-2%20скрипта-yellow)](02-python-automation/)
[![ТЗ](https://img.shields.io/badge/ТЗ-1%20интеграция-green)](04-ai-integration-tz/)
[![Power BI](https://img.shields.io/badge/Power_BI-дашборд-orange)](03-powerbi-dashboard/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Виктор Гоман** — 7 лет в финансах и цифровизации.

- Управлял выручкой **5,5 млрд руб.**, автоматизировал **15+** процессов
- Внедрял ИИ в здравоохранение Москвы: от MVP до масштабирования в регионы РФ и СНГ
- Стек: **SQL**, **Python**, **Power BI**, **1С**

## Оглавление

- [Быстрый старт](#quickstart)
- [Примеры кода](#code-examples)
- [Структура репозитория](#repo-structure)
- [Лицензия и участие](#license-contrib)
- [Контакты](#contacts)

<a id="quickstart"></a>

## Быстрый старт

| Роль | Смотреть сюда |
|------|---------------|
| Финансовый аналитик | [01-sql-tariffs](01-sql-tariffs/) — расчёт тарифов; [09-unit-economics](09-unit-economics/) — unit-экономика |
| Менеджер ИИ-проектов | [04-ai-integration-tz](04-ai-integration-tz/) — ТЗ на интеграцию с ЕМИАС; [05-json-configs](05-json-configs/) — конфиги моделей |
| Бизнес-аналитик IT | [02-python-automation](02-python-automation/) — автоматизация расчётов; [15-api-docs](15-api-docs/) — описание API |

<a id="code-examples"></a>

## Примеры кода

### SQL: расчёт тарифов ОЭЗ

См. [01-sql-tariffs/tariff_calculation.sql](01-sql-tariffs/tariff_calculation.sql) и соседние запросы в той же папке: оконные функции, **JOIN** нескольких сущностей биллинга, агрегация по **15+** видам услуг.

### Python: автоматизация расчётов

См. [02-python-automation/auto_calc.py](02-python-automation/auto_calc.py) — `pandas`, `openpyxl`, цепочка **1С → Excel → проверка → результат** (обезличенные поля).

```bash
pip install pandas openpyxl numpy
python auto_calc.py --input input_example.xlsx
```

### ТЗ: интеграция ИИ-браслетов с ЕМИАС

См. [04-ai-integration-tz/tz_emias_integration.md](04-ai-integration-tz/tz_emias_integration.md) — REST API, JSON-форматы, сценарии ошибок, критерии приёмки; в папке — дополнительные материалы согласования с клиниками.

<a id="repo-structure"></a>

## Структура репозитория (20 блоков)

| Папка | Содержание |
|-------|------------|
| [01-sql-tariffs](01-sql-tariffs/) | Рабочие SQL-образцы тарифного контура ОЭЗ |
| [02-python-automation](02-python-automation/) | Скрипты расчётов и примеры входных Excel |
| [03-powerbi-dashboard](03-powerbi-dashboard/) | Материалы дашборда и модель данных |
| [04-ai-integration-tz](04-ai-integration-tz/) | ТЗ ЕМИАС и приложения |
| [05-json-configs](05-json-configs/) | Конфиги ИИ-сервисов, версии после ревью |
| [06-debt-analysis](06-debt-analysis/) | Jupyter: дебиторка, эффект автоматизации |
| [07-grant-proposal](07-grant-proposal/) — [20-sql-interview](20-sql-interview/) | Остальные кейсы портфолио |

<a id="license-contrib"></a>

## Лицензия и участие

- [LICENSE](LICENSE) — **MIT**; код и запросы для ознакомления, рабочие данные обезличены, NDA соблюдены.  
- [CONTRIBUTING.md](CONTRIBUTING.md) — как предлагать мелкие правки к портфолио.

<a id="contacts"></a>

## Контакты

- **HeadHunter:** актуальное резюме — по запросу (ссылку обновляю в профиле HH).  
- **Email:** viktor.goman@list.ru  
- **Телефон:** +7 (985) 999-95-62  
- **Telegram:** @viktor_goman  
