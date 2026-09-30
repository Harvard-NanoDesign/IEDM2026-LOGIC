#!/usr/bin/env python3
# Copyright (c) 2026 Harvard University
# SPDX-License-Identifier: MIT
"""Count process steps per category from the detailed flows.

Inputs:  carbon_embodied/process_flows/<FLOW>_detailed_flow.csv
Outputs: outputs/process_steps.csv          FEOL + BEOL steps per category, with TOTAL
         outputs/feol_beol_step_counts.csv  FEOL and BEOL steps per category, with totals
"""
from common import CATEGORIES, FLOWS, combined, totals, write_table


def main():
    steps = totals("Step Count")
    both = combined(steps)
    total = {f: int(sum(both[f][c] for c in CATEGORIES)) for f in FLOWS}
    rows = [[c, *(int(both[f][c]) for f in FLOWS)] for c in CATEGORIES]
    rows.append(["TOTAL", *(total[f] for f in FLOWS)])
    write_table("process_steps.csv", ["category"], rows)

    rows = []
    for section in ("FEOL", "BEOL"):
        rows += [[section, c, *(int(steps[f][(section, c)]) for f in FLOWS)] for c in CATEGORIES]
        rows.append([section, "TOTAL", *(int(sum(steps[f][(section, c)] for c in CATEGORIES)) for f in FLOWS)])
    write_table("feol_beol_step_counts.csv", ["section", "category"], rows)

    # Steps outside the categories (TCAD Wafer steps) have no energy and set the wafer count.
    other = {f: int(sum(v for c, v in both[f].items() if c not in CATEGORIES)) for f in FLOWS}
    print("Total steps: " + ", ".join(f"{f} {total[f]}" for f in FLOWS))
    print("Uncategorised (Wafer) steps: " + ", ".join(f"{f} {other[f]}" for f in FLOWS))


if __name__ == "__main__":
    main()
