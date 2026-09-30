# IEDM2026-LOGIC

## Summary

Computing's *carbon footprint* has become a major consideration when designing future generations of VLSI circuits, accounting for both *embodied carbon* (C<sub>embodied</sub>) due to Integrated Circuit (IC) fabrication, and *operational carbon* (C<sub>operational</sub>) due to day-to-day use. In this paper, we quantify *trade-offs* in power, performance, area, and total carbon footprint (tC = C<sub>embodied</sub> + C<sub>operational</sub>, in kilograms of CO<sub>2</sub> equivalent) of next directions in FET technologies for high performance digital VLSI logic circuits. Specifically, we analyze the impact of advancing from today's FinFETs (FF) to each of *3* types of gate-all-around FETs:
(1) Nanosheet (NSH) FETs;
(2) *Sequential* Complementary FETs (*s*CF), in which NMOS & PMOS NSHFETs are fabricated on separate substrates that are subsequently bonded together; and
(3) *Monolithic* Complementary FETs (*m*CF), in which NMOS & PMOS NSHFETs are fabricated on the same starting substrate.

We develop detailed models to quantify C<sub>embodied</sub> for each direction, accounting for energy, material, and gas use from more than 500 individual process steps in complete fabrication processes. We then leverage industry-standard VLSI design flows to create full physical designs of a processor core (ARM Cortex-M0) using each FET technology and quantify power, performance, area, and C<sub>operational</sub> allowing us to optimize overall tCDP.

## Repository layout

| Path | Contents |
| --- | --- |
| `carbon_embodied/process_flows/` | Detailed process flows (`<FLOW>_detailed_flow.csv`) and deposited material masses (`<FLOW>_materials.csv`) for FF, NSH, sCF, and mCF. |
| `carbon_embodied/carbon_configuration/` | Configuration files (`config_epw.yaml`, `config_gpw.yaml`, `config_mpw.yaml`) with the energy, gas, and material emission factors. |
| `summary/` | Published summary tables: `epw.csv`, `mpw.csv`, `gpw.csv`, and `process_steps.csv` give the energy-per-wafer emissions, material-per-wafer emissions, gas-per-wafer emissions, and process-step counts, respectively, for each technology. These are the outputs of the scripts below; `epw.csv` excludes the 40% facility overhead. |
| `outputs/` | Script outputs |
| `power_performance_area_total_carbon/` | `PPAtC.csv`: power, performance, area, and total carbon for every ARM Cortex-M0 physical design. |
| `common.py`, `count_steps.py`, `epw.py`, `gpw.py`, `mpw.py` | Scripts that compute the step counts, EPW, GPW, and MPW from the process flows and configurations. |
| `run_all.sh` | Runs all four scripts in order. |

## Running the scripts

The scripts need Python 3.8 or later and use only the standard library. Run them from any directory:

```bash
python3 count_steps.py   # process-step counts per process area
python3 epw.py           # energy per wafer (EPW)
python3 gpw.py           # direct gas emissions per wafer (GPW)
python3 mpw.py           # materials and input gases per wafer (MPW)
```

Or run all four in order with `./run_all.sh`.

Each script prints its per-wafer totals and writes CSV tables to `outputs/`. The repository includes the outputs of a full run, so rerunning the scripts with the default configurations reproduces the files in `outputs/`:

| Script | Output files |
| --- | --- |
| `count_steps.py` | `process_steps.csv`, `feol_beol_step_counts.csv` |
| `epw.py` | `epw.csv` (kgCO<sub>2</sub>e per process area, without facility overhead), `epw_kwh.csv` (kWh per FEOL/BEOL process area, plus totals with the 40% facility overhead) |
| `gpw.py` | `gpw.csv` (kgCO<sub>2</sub>e per gas) |
| `mpw.py` | `mpw.csv` (kgCO<sub>2</sub>e per material category) |

C<sub>embodied</sub> per wafer is EPW (including facility overhead) + MPW + GPW. For FF this gives 350.19 + 41.57 + 112.52 = 504.28 kgCO<sub>2</sub>e/wafer, the value used in `PPAtC.csv`. The tables in `summary/` and the C<sub>embodied</sub> columns of `PPAtC.csv` match the script outputs. To change an assumption, such as the fab carbon intensity or the facility overhead, edit the matching file in `carbon_embodied/carbon_configuration/` and rerun the script.

## Citation

D. Kong, D. Grey-Stewart, M. Elgamal, Z. Chen, Z. Piao, J. Morris, Y. Yao, and G. Hills, “Quantifying Trade-Offs in Power, Performance, Area, and Total Carbon Footprint (PPAtC) of Next Directions in FET Technologies for VLSI Digital Logic Circuits,” *2026 IEEE International Electron Devices Meeting (IEDM)*, San Francisco, CA, USA, 2026, pp. 1-4.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
