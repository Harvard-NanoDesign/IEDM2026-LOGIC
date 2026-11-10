# CarbonEDA configuration

These files are the [CarbonEDA](https://github.com/Harvard-NanoDesign/CarbonEDA) configuration that the carbon results in `../outputs/logic/` were computed with (CarbonEDA v0, commit `310762a`). They replace the files of the same name in CarbonEDA's `config/` folder.

| File | Contents |
| --- | --- |
| `carbon_config.yaml` | Tool energy per step, input gases, and gas emissions for each process area, plus the fab carbon intensity (CI<sub>fab</sub> = 430 gCO<sub>2</sub>e/kWh) and the 40% facility overhead used for EPW. |
| `materials.yaml` | Density and GWP of each deposited material and wafer, the wafer diameter (300 mm), and yield (100%). |

The process flows these settings apply to are in `../technologies/logic/`. See [Reproducing the results](../README.md#reproducing-the-results) to rerun CarbonEDA with them.
