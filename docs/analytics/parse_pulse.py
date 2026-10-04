#!/usr/bin/env python3
"""Parse Leads Market weekly pulse.xlsx into analytics artifacts.

Usage:
    python3 docs/analytics/parse_pulse.py /path/to/pulse.xlsx

Outputs (next to this script):
    geo-matrix.csv
    directions-summary.md
    directions-summary.json

Requirements: openpyxl
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import openpyxl
except ImportError:  # pragma: no cover
    sys.exit("openpyxl is required: pip install openpyxl")

STOP_SHEET = "СТОП-ФАКТОРЫ"
TITLE_RE = re.compile(r"^([А-ЯA-Z]+)\s*-\s*(.+?)(\s*\((?:БТ|МНЧ)\))?\s*$")
PAREN_RE = re.compile(r"\(([^)]+)\)")


def parse(path: str, out_dir: Path) -> dict:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows_out: list[list] = []
    summary: list[dict] = []

    for ws in wb.worksheets:
        if ws.title == STOP_SHEET:
            continue
        sheet_rows = list(ws.iter_rows(values_only=True))
        if not sheet_rows:
            continue
        title = str(sheet_rows[0][0] or ws.title)
        m = TITLE_RE.match(title)
        code = m.group(1) if m else ws.title
        name = m.group(2).strip() if m else title
        block = "БТ" if "(БТ)" in title else ("МНЧ" if "(МНЧ)" in title else "")

        statuses: Counter = Counter()
        week_on: list[str] = []
        week_off: list[str] = []
        for row in sheet_rows[2:]:
            if not row or not row[0]:
                continue
            city = str(row[0]).strip()
            if city.lower().startswith("город"):
                continue
            status = str(row[1]).strip() if len(row) > 1 and row[1] else ""
            changed = str(row[2]).strip() if len(row) > 2 and row[2] else ""
            prev = str(row[3]).strip() if len(row) > 3 and row[3] else ""
            parent_match = PAREN_RE.search(city)
            parent = parent_match.group(1).strip() if parent_match else city
            rows_out.append([
                code, name, block, ws.title, city, parent,
                "да" if parent_match else "нет", status, changed, prev,
            ])
            statuses[status] += 1
            if len(row) > 6 and row[6]:
                week_off.append(str(row[6]).strip())
            if len(row) > 7 and row[7]:
                week_on.append(str(row[7]).strip())

        inc = statuses.get("Увеличить", 0)
        nochange = statuses.get("без изменений", 0)
        summary.append({
            "code": code,
            "sheet": ws.title,
            "name": name,
            "block": block,
            "total": sum(statuses.values()),
            "increase": inc,
            "nochange": nochange,
            "disable": statuses.get("Отключить", 0),
            "active_strict": inc,
            "active_loose": inc + nochange,
            "week_on": week_on,
            "week_off": week_off,
        })

    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "geo-matrix.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "direction_code", "direction_name", "block", "sheet", "city",
            "parent_department", "is_satellite", "status", "changed_flag", "prev_status",
        ])
        w.writerows(rows_out)

    with open(out_dir / "directions-summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    with open(out_dir / "directions-summary.md", "w", encoding="utf-8") as f:
        f.write("| Код | Направление | Блок | Всего | Увеличить | Без изм. | Отключить | Актив (строго) | Актив (строго+без изм.) |\n")
        f.write("|---|---|---|---:|---:|---:|---:|---:|---:|\n")
        for s in summary:
            f.write(
                f"| {s['code']} | {s['name']} | {s['block']} | {s['total']} | "
                f"{s['increase']} | {s['nochange']} | {s['disable']} | "
                f"{s['active_strict']} | {s['active_loose']} |\n"
            )
        f.write(
            f"\n**Итого:** строк {sum(s['total'] for s in summary)}, "
            f"Увеличить {sum(s['increase'] for s in summary)}, "
            f"без изменений {sum(s['nochange'] for s in summary)}, "
            f"Отключить {sum(s['disable'] for s in summary)}.\n"
        )
    return {"rows": len(rows_out), "directions": len(summary)}


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    out_dir = Path(__file__).resolve().parent
    result = parse(sys.argv[1], out_dir)
    print(f"Wrote to {out_dir}: rows={result['rows']}, directions={result['directions']}")


if __name__ == "__main__":
    main()
