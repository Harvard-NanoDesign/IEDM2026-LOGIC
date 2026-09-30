# Process flows

This folder contains the fabrication process flows from [1] for the four FET technologies: FF (FinFET baseline), NSH (nanosheet), sCF (sequential CFET), and mCF (monolithic CFET).

## `<FLOW>_detailed_flow.csv`

The complete process flow, with one row per process step or group of repeated steps. Each row gives:

- `FEOL/BEOL`: front-end-of-line or back-end-of-line section
- `MODULE`, `PITCH (nm)`, `LITHO METHOD`, `Process Description`: where the step sits in the flow and what it does
- `Category`: one of the 9 process areas (`Dry_etch`, `Metallization`, `Wet_etch`, `Deposition`, `EUV`, `ArFi_LE`, `ArF_LE`, `KrF`, `HG`), or `Wafer` for a starting or bonded substrate
- `Step Count`, `Energy/Step (kWh)`, `Total Energy (kWh)`: `Energy/Step (kWh)` is the value for the step's `Category` in `../carbon_configuration/config_epw.yaml`, and `Total Energy (kWh)` is `Step Count` × `Energy/Step (kWh)`

`count_steps.py`, `epw.py`, `gpw.py`, and `mpw.py` compute their results from the `Category` and `Step Count` columns.

## `<FLOW>_materials.csv`

The masses of the materials deposited in each flow, extracted from the 3D process simulation in Synopsys Sentaurus Process Explorer (SPX). Each row gives a material's total deposited thickness (nm), mass (g), GWP<sub>100</sub> characterization factor (kgCO<sub>2</sub>e/kg), and its resulting contribution to materials per wafer (`mpw_kgco2e`). `mpw.py` sums `mpw_kgco2e` to get the `chemicals` term of MPW.

## References

[1] D. Kong *et al.*, "Quantifying trade-offs in power, performance, area, and total carbon footprint (PPAtC) of next directions in FET technologies for VLSI digital logic circuits," in *IEDM Tech. Dig.*, San Francisco, CA, USA, Dec. 2026.
