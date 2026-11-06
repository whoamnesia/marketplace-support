#!/usr/bin/env python3
"""astudio-marketplace-support · deadlines.py — consumer-law deadlines for a remote purchase.

  python3 deadlines.py --delivered 2026-10-20 [--return-info-given yes|no] [--demand 2026-10-25] [--complex yes]

Prints the dates that follow from ЗоЗПП (ст. 18, 22, 25, 26.1) with the article for each.
Reference only, not legal advice: disputes go to a person. Calendar days; if the last day is a
non-working day the deadline moves to the next working day (ГК ст. 193) — the script flags weekends,
holidays must be checked by a person.
"""
import argparse, datetime as dt, sys

def d(s): return dt.date.fromisoformat(s)

def add_months(day, n):
    m = day.month - 1 + n; y = day.year + m // 12; m = m % 12 + 1
    import calendar
    return dt.date(y, m, min(day.day, calendar.monthrange(y, m)[1]))

def fmt(x):
    note = " (выходной: срок переносится на следующий рабочий день, ст. 193 ГК)" if x.weekday() >= 5 else ""
    return x.strftime("%d.%m.%Y") + note

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--delivered", required=True); ap.add_argument("--return-info-given", default="yes", choices=["yes", "no"])
    ap.add_argument("--demand"); ap.add_argument("--complex", default="no", choices=["yes", "no"])
    a = ap.parse_args()
    dl = d(a.delivered)
    print(f"Товар получен: {dl.strftime('%d.%m.%Y')}")
    if a.return_info_given == "yes":
        print(f"- Отказ от товара надлежащего качества (ст. 26.1 п. 4): до {fmt(dl + dt.timedelta(days=7))} включительно")
    else:
        print(f"- Отказ от товара надлежащего качества (ст. 26.1 п. 4, информация о возврате не дана): до {fmt(add_months(dl, 3))}")
    print("  Способ возврата выбирает покупатель, если продавец может проверить товар при получении (КС РФ 7-П от 17.02.2026).")
    print(f"- Обмен товара надлежащего качества (ст. 25, если применимо): до {fmt(dl + dt.timedelta(days=14))}")
    if a.complex == "yes":
        print(f"- Технически сложный товар с недостатком (ст. 18 п. 1): возврат или замена по любому недостатку до {fmt(dl + dt.timedelta(days=15))}; позже — только при существенном недостатке, нарушении сроков ремонта или >30 дней без использования в году гарантии")
    if a.demand:
        dm = d(a.demand)
        print(f"Требование предъявлено: {dm.strftime('%d.%m.%Y')}")
        print(f"- Возврат денег при отказе от дистанционной покупки (ст. 26.1 п. 4): до {fmt(dm + dt.timedelta(days=10))}")
        print(f"- Возврат денег / уменьшение цены за недостаток (ст. 22): до {fmt(dm + dt.timedelta(days=10))}")
        print(f"- Замена товара с недостатком (ст. 21): до {fmt(dm + dt.timedelta(days=7))}, если нужна проверка качества — до {fmt(dm + dt.timedelta(days=20))}")
    print("\nСправка, не юридическая консультация. Спор, отказ или претензию решает человек.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
