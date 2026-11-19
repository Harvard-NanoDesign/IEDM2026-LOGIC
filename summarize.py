# Copyright (c) 2026 Harvard University
# SPDX-License-Identifier: MIT
"""Collect the CarbonEDA carbon CSVs of the technologies into summary/ and update the C_embodied columns of PPAtC.csv."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUTS = HERE / "outputs" / "logic"
SUMMARY = HERE / "summary"
PPATC = HERE / "power_performance_area_total_carbon" / "PPAtC.csv"
TECHS = {"FF": "ff", "NSH": "nsh", "sCF": "scfet", "mCF": "mcfet"}
COLS = list(TECHS)
TOTALS = [("steps", "steps"), ("uncounted_steps", "steps"), ("carrier_wafers", "wafers"),
          ("tool_energy_kwh", "kWh"), ("energy_kwh", "kWh"),
          ("tool_epw_kgco2e", "kgCO2e"), ("overhead_epw_kgco2e", "kgCO2e"), ("epw_kgco2e", "kgCO2e"),
          ("mpw_material_kgco2e", "kgCO2e"), ("mpw_gas_kgco2e", "kgCO2e"), ("mpw_kgco2e", "kgCO2e"),
          ("gpw_kgco2e", "kgCO2e"), ("total_kgco2e", "kgCO2e"), ("total_kgco2e_per_good_wafer", "kgCO2e")]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(name: str, header: list[str], rows: list[list]) -> None:
    with (SUMMARY / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"wrote summary/{name}")


def carbon(tech: str, name: str) -> list[dict]:
    return read_csv(OUTPUTS / TECHS[tech] / "carbon" / f"{name}.csv")


def by_key(rows: dict[str, dict[str, float]]) -> list[list]:
    """{key: {tech: value}} as table rows, keys in first-seen order, 0 where a technology has none."""
    return [[key, *(values.get(c, 0) for c in COLS)] for key, values in rows.items()]


def main() -> None:
    SUMMARY.mkdir(exist_ok=True)
    totals = {c: {r["metric"]: float(r["value"]) for r in carbon(c, "totals")} for c in COLS}
    write_csv("totals.csv", ["metric", "unit", *COLS],
              [[m, unit, *(int(totals[c][m]) if unit in ("steps", "wafers") else totals[c][m] for c in COLS)]
               for m, unit in TOTALS])

    steps, epw = defaultdict(dict), defaultdict(dict)
    for c in COLS:
        for r in carbon(c, "by_area"):
            if r["process_area"] != "Wafer":
                steps[r["process_area"]][c] = int(r["steps"])
                epw[r["process_area"]][c] = float(r["epw_kgco2e"])
    write_csv("process_steps.csv", ["process_area", *COLS],
              by_key(steps) + [["TOTAL", *(int(totals[c]["steps"]) for c in COLS)]])
    write_csv("epw.csv", ["process_area", "unit", *COLS], [[k, "kgCO2e", *v] for k, *v in by_key(epw)])

    # MPW: starting and carrier wafers, deposited materials, and upstream production of each input gas
    mpw = defaultdict(dict)
    for c in COLS:
        for r in carbon(c, "steps"):
            key = "silicon_wafer" if r["process_area"] == "Wafer" else "materials"
            mpw[key][c] = mpw[key].get(c, 0.0) + float(r["mpw_material_kgco2e"] or 0)
        for r in carbon(c, "gases"):
            if r["role"] == "upstream":
                key = f"{r['gas']}_gas"
                mpw[key][c] = mpw[key].get(c, 0.0) + float(r["mpw_gco2e"]) / 1000.0
    write_csv("mpw.csv", ["material_category", "unit", *COLS], [[k, "kgCO2e", *v] for k, *v in by_key(mpw)])

    # GPW: each gas emitted after abatement, as unused input gas or as a byproduct
    gpw = defaultdict(dict)
    for c in COLS:
        for r in carbon(c, "gases"):
            if r["role"] != "upstream":
                key = (r["gas"], r["role"])
                gpw[key][c] = gpw[key].get(c, 0.0) + float(r["gpw_gco2e"]) / 1000.0
    write_csv("gpw.csv", ["gas", "role", "unit", *COLS],
              [[gas, role, "kgCO2e", *v] for (gas, role), *v in by_key(gpw)])

    # PPAtC: C_embodied per wafer and per good die from the new totals
    rows = read_csv(PPATC)
    for r in rows:
        per_wafer = totals[r["tech"]]["total_kgco2e"]
        r["cembodied_per_wafer_kgCO2e"] = per_wafer
        r["cembodied_gooddie"] = per_wafer / (float(r["good_die_per_wafer"]) * float(r["yield"]))
    with PPATC.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"updated {PPATC.relative_to(HERE)} ({len(rows)} designs)")
    for c in COLS:
        t = totals[c]
        print(f"{c:>4}: EPW {t['epw_kgco2e']:.2f} + MPW {t['mpw_kgco2e']:.2f} + GPW {t['gpw_kgco2e']:.2f} "
              f"= {t['total_kgco2e']:.2f} kgCO2e/wafer, {int(t['steps'])} steps")


if __name__ == "__main__":
    main()
