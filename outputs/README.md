# CarbonEDA outputs

Everything in this folder is output from [CarbonEDA](https://github.com/Harvard-NanoDesign/CarbonEDA) (v0, commit `310762a`), run on the process flows in `../technologies/logic/` with the configuration in `../config/`. It is copied unchanged from CarbonEDA's `outputs/logic/` folder. The `nsh`, `scfet`, and `mcfet` results were rerun on 11/9/2026 after the layout and BEOL via updates (see [Updates since the IEDM 2026 paper](../README.md#updates-since-the-iedm-2026-paper)), and `ff` after a shorter active-cut Si etch (step 610, 3 min instead of 11) that no longer undercuts the edge fins. All four use the same carbon code and configuration as v0, their carbon per wafer is unchanged, and their design-review PDFs were generated with this CarbonEDA commit.

Each technology (`ff`, `nsh`, `scfet`, `mcfet`) has two folders:

| Path | Contents |
| --- | --- |
| `logic/<tech>/carbon/` | Carbon results from `make carbon`: `steps.csv` (EPW, MPW, and GPW per process step), `gases.csv` (per gas and step), `by_module.csv`, `by_area.csv`, and `totals.csv`. All values are per 300 mm wafer, with the unit in each column name. |
| `logic/<tech>/report/` | `<tech>_design_review.pdf` from `make all`: one page per process step with its 3D structure from the Sentaurus Process Explorer simulation, cross-sections, mask, materials, and EPW, MPW, and GPW, plus summaries by module and process area. |

`../summarize.py` combines these results into `../summary/` and the C<sub>embodied</sub> columns of `../power_performance_area_total_carbon/PPAtC.csv`.
