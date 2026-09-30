#!/usr/bin/env python3
# Copyright (c) 2026 Harvard University
# SPDX-License-Identifier: MIT
"""Materials per wafer (MPW): wafers, deposited materials and upstream gas production.

  silicon_wafer  wafer_kgco2e x Wafer steps in the flow (substrate / carrier wafers)
  chemicals      sum of mpw_kgco2e in carbon_embodied/process_flows/<FLOW>_materials.csv
  <gas>_gas      kg gas/step x kgCO2e/kg x the flow's steps in that category (FEOL + BEOL)

Inputs:  carbon_embodied/process_flows/<FLOW>_detailed_flow.csv
         carbon_embodied/process_flows/<FLOW>_materials.csv
         carbon_embodied/carbon_configuration/config_mpw.yaml
Outputs: outputs/mpw.csv       kgCO2e per material category
"""
from common import FLOWS, FLOWS_DIR, combined, read_config, read_csv, totals, write_table


def main():
    config = read_config("config_mpw.yaml")
    counts = combined(totals("Step Count"))
    mpw = {
        "silicon_wafer": {f: config["wafer_kgco2e"] * counts[f].get("Wafer", 0) for f in FLOWS},
        "chemicals": {f: sum(float(r["mpw_kgco2e"]) for r in read_csv(FLOWS_DIR / f"{f}_materials.csv"))
                      for f in FLOWS},
    }
    for gas, g in config["upstream_gases"].items():
        per_step = g["kg_gas_per_step"] * g["kgco2e_per_kg_gas"]
        mpw[gas] = {f: per_step * counts[f].get(g["step_category"], 0) for f in FLOWS}
    write_table("mpw.csv", ["material_category", "unit"],
                [[name, "kgCO2e", *(v[f] for f in FLOWS)] for name, v in mpw.items()])
    print("MPW total (kgCO2e/wafer): " + ", ".join(
        f"{f} {sum(v[f] for v in mpw.values()):.2f}" for f in FLOWS))


if __name__ == "__main__":
    main()
