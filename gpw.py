#!/usr/bin/env python3
# Copyright (c) 2026 Harvard University
# SPDX-License-Identifier: MIT
"""Gases per wafer (GPW): direct process-gas emissions after abatement.

Each gas = sum over step categories of kgCO2e/step
(carbon_embodied/carbon_configuration/config_gpw.yaml) x the flow's steps in that
category (dry etch and deposition, FEOL + BEOL).

Inputs:  carbon_embodied/process_flows/<FLOW>_detailed_flow.csv
         carbon_embodied/carbon_configuration/config_gpw.yaml
Outputs: outputs/gpw.csv       kgCO2e per gas
"""
from common import FLOWS, combined, read_config, totals, write_table


def main():
    gases = read_config("config_gpw.yaml")["gases_kgco2e_per_step"]
    counts = combined(totals("Step Count"))
    gpw = {gas: {f: sum(value * counts[f].get(step, 0) for step, value in factors.items()) for f in FLOWS}
           for gas, factors in gases.items()}
    write_table("gpw.csv", ["gas", "unit"], [[gas, "kgCO2e", *(v[f] for f in FLOWS)] for gas, v in gpw.items()])
    print("GPW total (kgCO2e/wafer): " + ", ".join(
        f"{f} {sum(v[f] for v in gpw.values()):.2f}" for f in FLOWS))


if __name__ == "__main__":
    main()
