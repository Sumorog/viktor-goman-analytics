# -*- coding: utf-8 -*-
"""
Генерация визуальных артефактов портфолио:
- 03-powerbi-dashboard/dashboard_screenshot.png — учебный дашборд (структура как в Power BI)
- 03-powerbi-dashboard/data_model.png — схема звезды (упрощённо)
- 10-presentation-muf2023/slides.pdf — 3 обезличенных слайда

Данные для графиков: фрагмент, стилизованный под открытые данные Портала data.mos.ru
(без API-ключа; для «живых» данных см. README в 03 — переменная MOS_DATA_API_KEY).
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parents[1]
DIR03 = ROOT / "03-powerbi-dashboard"
DIR10 = ROOT / "10-presentation-muf2023"

# Учебный набор: округ / условный показатель (не претендует на официальную статистику)
SAMPLE_PATH = DIR03 / "sample_mos_open_style.json"


def write_sample_json():
    data = [
        {"district": "ЦАО", "requests": 1240, "satisfaction": 4.1},
        {"district": "САО", "requests": 980, "satisfaction": 4.0},
        {"district": "СВАО", "requests": 1120, "satisfaction": 3.9},
        {"district": "ВАО", "requests": 860, "satisfaction": 3.8},
        {"district": "ЮВАО", "requests": 910, "satisfaction": 3.9},
        {"district": "ЮАО", "requests": 1050, "satisfaction": 4.0},
        {"district": "ЮЗАО", "requests": 1180, "satisfaction": 4.1},
        {"district": "ЗАО", "requests": 790, "satisfaction": 4.0},
        {"district": "СЗАО", "requests": 1020, "satisfaction": 3.9},
        {"district": "ЗелАО", "requests": 340, "satisfaction": 4.2},
        {"district": "ТиНАО", "requests": 720, "satisfaction": 3.7},
    ]
    SAMPLE_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def render_dashboard_png():
    rows = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    districts = [r["district"] for r in rows]
    requests = [r["requests"] for r in rows]
    sat = [r["satisfaction"] for r in rows]

    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor("#f4f6f8")
    fig.suptitle(
        "Учебный дашборд (визуализация в стиле Power BI)\n"
        "Источник данных: демо-набор в формате открытых данных (структура как у data.mos.ru)",
        fontsize=14,
        fontweight="bold",
        color="#1a1a1a",
    )

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.barh(districts[::-1], requests[::-1], color="#2b6cb0")
    ax1.set_title("Количество обращений по округам (демо)")
    ax1.set_xlabel("Обращения, шт.")

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(districts, sat, marker="o", color="#c05621", linewidth=2)
    ax2.set_title("Средняя оценка удовлетворённости (демо, 1–5)")
    ax2.set_ylabel("Балл")
    ax2.tick_params(axis="x", rotation=45)

    ax3 = fig.add_subplot(2, 1, 2)
    cum = []
    s = 0
    for v in requests:
        s += v
        cum.append(s)
    ax3.fill_between(range(len(districts)), cum, color="#38a169", alpha=0.35)
    ax3.plot(range(len(districts)), cum, color="#276749", linewidth=2)
    ax3.set_xticks(range(len(districts)))
    ax3.set_xticklabels(districts, rotation=45, ha="right")
    ax3.set_title("Накопительный итог обращений (демо)")
    ax3.set_ylabel("Сумма, шт.")

    metrics = (
        "Метрики на скриншоте: обращения по территории, satisfaction, кумулятив.\n"
        "Для продакшена: меры DAX + RLS; здесь — matplotlib как «макет» для портфолио."
    )
    fig.text(0.5, 0.02, metrics, ha="center", fontsize=9, color="#4a5568")

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    out = DIR03 / "dashboard_screenshot.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


def render_data_model_png():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("Упрощённая схема модели (звезда) — учебный макет", fontsize=13, pad=12)

    def box(x, y, w, h, label, color):
        ax.add_patch(
            plt.Rectangle((x, y), w, h, fill=True, facecolor=color, edgecolor="#1a202c", linewidth=1.5)
        )
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9, color="white", fontweight="bold")

    box(4, 5, 2, 1.2, "Fact\nRequests", "#2b6cb0")
    box(1, 2, 1.8, 1, "Dim\nDistrict", "#805ad5")
    box(4, 2, 1.8, 1, "Dim\nDate", "#d69e2e")
    box(7, 2, 1.8, 1, "Dim\nChannel", "#319795")

    for x1, y1, x2, y2 in [(5, 5, 1.9, 2.5), (5, 5, 4.9, 2.5), (5, 5, 7.9, 2.5)]:
        ax.plot([5, x1], [5, y1], color="#718096", linewidth=1.2)

    ax.text(5, 8.2, "Связи: многие-к-одному в факт", ha="center", fontsize=10, color="#2d3748")
    out = DIR03 / "data_model.png"
    fig.savefig(out, dpi=120, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", out)


def render_slides_pdf():
    out = DIR10 / "slides.pdf"
    with PdfPages(out) as pdf:
        for title, bullets in [
            (
                "Цифровизация городских сервисов: уроки пилота",
                [
                    "Обезличенные кейсы: от MVP к промышленной эксплуатации",
                    "Единый контракт API — масштабирование в регионы РФ и СНГ",
                    "Метрики: SLA, время ответа, удовлетворённость пользователей",
                ],
            ),
            (
                "ИИ и ПДн: что согласовывать до разработки",
                [
                    "Минимизация данных, маскирование в логах",
                    "Критерии приёмки и сценарии отказа шины",
                    "Согласование с клиниками / заказчиком — протокол UAT",
                ],
            ),
            (
                "Роль аналитика на стыке финансов и ИТ",
                [
                    "От тарифов (5,5 млрд портфель) — к продуктовой аналитике ИИ",
                    "SQL + Python + Power BI + документация требований",
                    "Контакты: см. README репозитория",
                ],
            ),
        ]:
            fig, ax = plt.subplots(figsize=(11, 8.5))
            ax.axis("off")
            ax.set_facecolor("#1a365d")
            fig.patch.set_facecolor("#1a365d")
            ax.text(
                0.08,
                0.88,
                title,
                fontsize=22,
                color="white",
                fontweight="bold",
                transform=ax.transAxes,
            )
            y = 0.72
            for line in bullets:
                ax.text(
                    0.1,
                    y,
                    "• " + line,
                    fontsize=14,
                    color="#e2e8f0",
                    transform=ax.transAxes,
                    wrap=True,
                )
                y -= 0.12
            ax.text(
                0.08,
                0.06,
                "Moscow Urban Forum — стиль слайдов (обезличенный учебный макет)",
                fontsize=10,
                color="#a0aec0",
                transform=ax.transAxes,
            )
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
    print("wrote", out)


def main():
    os.makedirs(DIR03, exist_ok=True)
    os.makedirs(DIR10, exist_ok=True)
    write_sample_json()
    render_dashboard_png()
    render_data_model_png()
    render_slides_pdf()


if __name__ == "__main__":
    main()
