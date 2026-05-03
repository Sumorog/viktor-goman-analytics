#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания структуры портфолио на GitHub
Автор: я сам, GPT не писал (шутка, но код правил руками)
TODO: добавить argparse, пока так
"""

import os
import shutil

# === НАСТРОЙКИ ===
# путь куда создавать — поменяй на свой
BASE_DIR = "./viktor-goman-analytics"  
# если папка есть — удалим и создадим заново (осторожно!)
CLEAN_START = True

# === СТРУКТУРА ===
# список: (папка, описание для README)
PROJECTS = [
    ("01-sql-tariffs", "SQL-запросы для расчёта тарифов ОЭЗ. Примеры JOIN, оконных функций, агрегации."),
    ("02-python-automation", "Автоматизация расчётов 15+ видов услуг. pandas, openpyxl, интеграция с 1С."),
    ("03-powerbi-dashboard", "Дашборд для мониторинга выручки и загрузки. DAX, модель данных."),
    ("04-ai-integration-tz", "ТЗ на интеграцию ИИ-браслетов с ЕМИАС. REST API, форматы данных."),
    ("05-json-configs", "JSON-конфиги для настройки ИИ-моделей. Примеры валидации схем."),
    ("06-debt-analysis", "Анализ дебиторской задолженности. Прогноз, сегментация, автоматизация уведомлений."),
    ("07-grant-proposal", "Часть грантовой заявки по прогнозированию закупок. Методология."),
    ("08-crm-requirements", "Требования к CRM для малого бизнеса. User stories, acceptance criteria."),
    ("09-unit-economics", "Расчёт unit-экономики услуг. CAC, LTV, маржинальность."),
    ("10-presentation-muf2023", "Материалы выступления Moscow Urban Forum 2023. Обезличенные слайды."),
    ("11-1c-integration", "Формат обмена данными с 1С. XML, структуры таблиц."),
    ("12-data-cleaning", "Очистка и валидация данных. pandas, регулярные выражения."),
    ("13-ab-test-analysis", "Анализ A/B теста тарифных изменений. Статистика, доверительные интервалы."),
    ("14-forecasting", "Прогнозирование выручки. Временные ряды, скользящее среднее."),
    ("15-api-docs", "Документация API для интеграции. Endpoints, примеры запросов."),
    ("16-risk-matrix", "Матрица рисков проекта внедрения ИИ. Вероятность, влияние, митигация."),
    ("17-kpi-dashboard", "Трекер KPI команды. Автоматический расчёт из сырых данных."),
    ("18-process-map", "Карта бизнес-процесса тарифного планирования. AS-IS / TO-BE."),
    ("19-chatbot-logic", "Логика работы ИИ-ассистента для записи. Дерево сценариев."),
    ("20-sql-interview", "Типовые SQL-задачи с собеседований. Решения с объяснениями."),
]

# === ГЛАВНЫЙ README ===
# костыль: просто многострочная строка, потом запишем
MAIN_README = """# Портфолио аналитика

**Виктор Гоман** — финансовый аналитик с экспертизой в цифровизации.

- 7 лет опыта: от тарифной политики с выручкой 5,5 млрд руб. до внедрения ИИ в здравоохранение
- Стек: SQL, Python, Power BI, 1С
- Город: Москва, готов к релокации и удалёнке

## Структура

| Папка | Описание |
|-------|----------|
"""

# дополним таблицей — ниже в коде

# === КОД ===

def create_structure():
    """Создаёт всю структуру папок и файлов"""
    
    # чистим если надо
    if CLEAN_START and os.path.exists(BASE_DIR):
        print(f"[!] Удаляем старую папку {BASE_DIR}")
        shutil.rmtree(BASE_DIR)
    
    os.makedirs(BASE_DIR, exist_ok=True)
    print(f"[+] Создана базовая папка: {BASE_DIR}")
    
    # собираем строки для главного README
    table_lines = []
    
    for folder, desc in PROJECTS:
        # создаём папку
        folder_path = os.path.join(BASE_DIR, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # README в папке
        readme_path = os.path.join(folder_path, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {folder}\n\n")
            f.write(f"{desc}\n\n")
            f.write("## Статус\n\n")
            f.write("- [ ] Добавить код/данные\n")
            f.write("- [ ] Добавить описание шагов\n")
            f.write("- [ ] Проверить на читаемость\n\n")
            f.write("## Файлы\n\n")
            f.write("(пока пусто, заполняю)\n")
        
        # добавляем строку в таблицу главного README
        table_lines.append(f"| {folder} | {desc} |")
        
        print(f"[+] Создана папка: {folder}")
    
    # пишем главный README
    main_readme_path = os.path.join(BASE_DIR, "README.md")
    with open(main_readme_path, "w", encoding="utf-8") as f:
        f.write(MAIN_README)
        for line in table_lines:
            f.write(line + "\n")
        f.write("\n## Контакты\n\n")
        f.write("- Email: viktor.goman@list.ru\n")
        f.write("- Telegram: @viktor_goman  # TODO: проверить username\n")
        f.write("- HeadHunter: [ссылка]  # TODO: добавить\n")
    
    print(f"[+] Главный README создан")
    print(f"\n[!] Итого папок: {len(PROJECTS)}")
    print("[!] Теперь заполняй содержимое — шаблоны ниже")

# === ЗАПУСК ===
if __name__ == "__main__":
    create_structure()
    print("\nГотово. Дальше — git init, git add, git commit, git push")
    print("Или просто drag-and-drop в GitHub Desktop")