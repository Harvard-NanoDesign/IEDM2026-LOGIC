# Carbon configuration

This folder contains the configuration files that `epw.py`, `gpw.py`, and `mpw.py` read to compute the embodied carbon of each process flow, following the method in [1].

| File | Used by | Contents |
| --- | --- | --- |
| `config_epw.yaml` | `epw.py` | Energy per wafer (EPW): tool energy per step (kWh) for each of the 9 process areas, the fab electricity carbon intensity (0.43 kgCO<sub>2</sub>e/kWh), and the facility overhead factor (1.4). |
| `config_gpw.yaml` | `gpw.py` | Gases per wafer (GPW): direct emissions per dry-etch or deposition step (kgCO<sub>2</sub>e/step) for each gas, after utilization and abatement. |
| `config_mpw.yaml` | `mpw.py` | Materials per wafer (MPW): embodied carbon of one 300 mm silicon wafer, and the mass and upstream GWP<sub>100</sub> of each input process gas (NF<sub>3</sub>, C<sub>4</sub>F<sub>8</sub>, SF<sub>6</sub>) per step. |

Each script multiplies these per-step factors by the step counts in `../process_flows/<FLOW>_detailed_flow.csv`. The files use plain `key: value` YAML mappings, and `common.py` parses them without needing PyYAML.

## References

[1] D. Kong *et al.*, "Quantifying trade-offs in power, performance, area, and total carbon footprint (PPAtC) of next directions in FET technologies for VLSI digital logic circuits," in *IEDM Tech. Dig.*, San Francisco, CA, USA, Dec. 2026.
