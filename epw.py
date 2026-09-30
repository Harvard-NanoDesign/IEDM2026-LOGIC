#!/usr/bin/env python3
# Copyright (c) 2026 Harvard University
# SPDX-License-Identifier: MIT
"""Energy per wafer (EPW) from the step counts in the detailed flows.

Each step's energy is its count x the BEOL-derived kWh/step for its category in
carbon_embodied/carbon_configuration/config_epw.yaml, converted to kgCO2e at the
fab carbon intensity.

Inputs:  carbon_embodied/process_flows/<FLOW>_detailed_flow.csv
         carbon_embodied/carbon_configuration/config_epw.yaml
Outputs: outputs/epw.csv       kgCO2e per category, FEOL + BEOL, no facility overhead
         outputs/epw_kwh.csv   kWh per FEOL/BEOL category, totals, facility overhead
                               and kgCO2e/wafer
"""
from common import CATEGORIES, FLOWS, combined, read_config, totals, write_table


def main():
    config = read_config("config_epw.yaml")
    ci_fab, overhead = config["ci_fab_kgco2e_per_kwh"], config["facility_overhead"]
    per_step = config["energy_per_step_kwh"]
    steps = totals("Step Count")
    kwh = {f: {(s, c): steps[f][(s, c)] * per_step[c]
               for s in ("FEOL", "BEOL") for c in CATEGORIES} for f in FLOWS}
    both = combined(kwh)
    write_table("epw.csv", ["process_area", "unit"],
                [[c, "kgCO2e", *(both[f][c] * ci_fab for f in FLOWS)] for c in CATEGORIES])

    total = {f: sum(both[f][c] for c in CATEGORIES) for f in FLOWS}
    rows = [[s, c, "kWh", *(kwh[f][(s, c)] for f in FLOWS)] for s in ("FEOL", "BEOL") for c in CATEGORIES]
    rows += [
        ["ALL", "TOTAL", "kWh", *(total[f] for f in FLOWS)],
        ["ALL", "TOTAL + facility", "kWh", *(total[f] * overhead for f in FLOWS)],
        ["ALL", "EPW incl. facility", "kgCO2e", *(total[f] * overhead * ci_fab for f in FLOWS)],
    ]
    write_table("epw_kwh.csv", ["section", "category", "unit"], rows)
    print("Tool energy (kWh/wafer): " + ", ".join(f"{f} {total[f]:.2f}" for f in FLOWS))
    print(f"EPW incl. {overhead - 1:.0%} facility at {ci_fab} kgCO2e/kWh (kgCO2e/wafer): "
          + ", ".join(f"{f} {total[f] * overhead * ci_fab:.2f}" for f in FLOWS))


if __name__ == "__main__":
    main()
