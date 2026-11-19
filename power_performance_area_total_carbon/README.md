# Power, performance, area, and total carbon (PPAtC)

`PPAtC.csv` lists the power, performance, area, and carbon footprint of every ARM Cortex-M0 physical design in [1]. Each row is one design: a combination of FET technology (FF, NSH, sCF, and mCF), supply voltage (V<sub>DD</sub>), threshold-voltage flavor (V<sub>T</sub>), and target clock frequency.

FF's C<sub>embodied</sub> is for its fabrication process with an EUV-patterned front end (see [Updates since the IEDM 2026 paper](../README.md#updates-since-the-iedm-2026-paper)), not the multi-patterned front end in [1]. This changes only the fabrication process, not the ASAP7 devices or standard cells, so the FF designs keep their power, performance, and area.

## Method

The data is generated in 4 steps.

1. **Quantify C<sub>embodied</sub> per wafer.** C<sub>embodied</sub> = C<sub>embodied,EPW</sub> + C<sub>embodied,MPW</sub> + C<sub>embodied,GPW</sub>, computed by [CarbonEDA](https://github.com/Harvard-NanoDesign/CarbonEDA) from the process flows in `../technologies/logic/` and the configuration in `../config/` (results in `../outputs/logic/` and `../summary/totals.csv`). EPW sums the tool energy of every step, multiplies it by 1.4 for fab facility overhead, and converts it at CI<sub>fab</sub> = 430 gCO<sub>2</sub>e/kWh (South Korea grid). MPW multiplies the mass of each deposited material, each starting and carrier wafer, and each input process gas by its upstream GWP<sub>100</sub>. GPW accounts for input process gases that are not utilized and for the byproduct gases the processes form, after abatement, using downstream GWP<sub>100</sub>.
2. **Characterize the standard cells.** Cadence Liberate characterizes timing and power for each standard-cell library at V<sub>DD</sub> = 0.6, 0.65, and 0.7 V and for the LVT, RVT, and HVT flavors. The SPICE compact models are from the ASAP7 predictive PDK [2] for FF and from Global TCAD Solutions [3] for NSH, sCF, and mCF. The standard-cell libraries are from ASAP7 [2] for FF, GT2N [4] for NSH, and [5] for sCF and mCF. sCF and mCF share the same standard-cell layouts, so they have the same power, performance, and area.
3. **Synthesize and place-and-route.** Cadence Genus and Innovus produce Cortex-M0 physical designs for each V<sub>DD</sub>, V<sub>T</sub>, and target clock frequency. Gate-level simulation in VCS produces switching activity for post-place-and-route power analysis in Innovus, which gives the energy per cycle, critical path delay, and area of each design.
4. **Quantify C<sub>operational</sub> and total carbon.** C<sub>operational</sub> is the energy of one run of the `matmult-int` benchmark from Embench [6] (20,047,348 cycles) multiplied by CI<sub>use</sub> = 380 gCO<sub>2</sub>e/kWh (average United States grid). C<sub>embodied</sub> per good die divides C<sub>embodied</sub> per wafer by the number of good dies per 300 mm wafer, at 90% yield.

## Columns

| Column | Unit | Description |
| --- | --- | --- |
| `tech` | | FET technology: `FF`, `NSH`, `sCF`, or `mCF` |
| `supply_voltage` | V | Supply voltage V<sub>DD</sub> |
| `flavor` | | Threshold-voltage flavor: `LVT`, `RVT`, or `HVT` |
| `tracks` | | Standard-cell height in metal tracks: `s7.5t` (FF), `s6t` (NSH), `s4t` (sCF and mCF). The count is the cell height in minimum metal pitches: NSH is 144 nm = 6 × 24 nm, and sCF and mCF are 96 nm = 4 × 24 nm (the GT2 CFET library calls this cell height `s3t`, after the 3 signal tracks between its power rails) |
| `area_um2` | µm² | Post-place-and-route die area (A) |
| `energy_per_cycle_fJ` | fJ | Energy per clock cycle running `matmult-int` |
| `critical_path_ps` | ps | Critical path delay |
| `yield` | | Die yield (Y), 0.9 for all designs |
| `good_die_per_wafer` | | Dies per 300 mm wafer before yield: π·d²/(4A) − π·d/√(2A), with d = 300 mm |
| `cembodied_per_wafer_kgCO2e` | kgCO<sub>2</sub>e | C<sub>embodied</sub> per wafer: EPW (with facility overhead) + MPW + GPW |
| `cembodied_gooddie` | kgCO<sub>2</sub>e | C<sub>embodied</sub> per good die: `cembodied_per_wafer_kgCO2e` / (`good_die_per_wafer` × `yield`) |
| `energy_per_run_fJ` | fJ | Energy per `matmult-int` run: `energy_per_cycle_fJ` × 20,047,348 |
| `cop_per_run_kgCO2e_USgrid` | kgCO<sub>2</sub>e | C<sub>operational</sub> per run: `energy_per_run_fJ` converted to kWh × 0.38 kgCO<sub>2</sub>e/kWh |

## Computing total carbon and tCDP

For a workload of N runs, the total carbon of one die is

```
tC = cembodied_gooddie + N × cop_per_run_kgCO2e_USgrid
```

and the total carbon delay product is

```
tCDP = tC × delay,  delay = 20,047,348 cycles × critical_path_ps
```

where delay is the runtime of one `matmult-int` run: its cycle count times the critical path delay (the clock period). [1] evaluates N = 10<sup>7</sup> runs, where C<sub>embodied</sub> dominates, and N = 10<sup>12</sup> runs, where C<sub>operational</sub> dominates, and sweeps N to find the tCDP-optimal design for each technology.

## References

[1] D. Kong *et al.*, "Quantifying trade-offs in power, performance, area, and total carbon footprint (PPAtC) of next directions in FET technologies for VLSI digital logic circuits," in *IEDM Tech. Dig.*, San Francisco, CA, USA, Dec. 2026.

[2] L. T. Clark *et al.*, "ASAP7: A 7-nm finFET predictive process design kit," *Microelectron. J.*, vol. 53, pp. 105–115, Jul. 2016, doi: 10.1016/j.mejo.2016.04.006.

[3] D. Yakimets, K. K. Bhuwalka, H. Wu, G. Rzepa, M. Karner, and C. Liu, "Inflection points in GAA NS-FET to C-FET scaling considering impact of DTCO boosters," *IEEE Trans. Electron Devices*, vol. 71, no. 4, pp. 2309–2314, Apr. 2024, doi: 10.1109/TED.2024.3368380.

[4] D. Jang *et al.*, "GT2N: An open-source 2nm nanosheet PDK enabling multi-width/VT benchmarking," in *Proc. IEEE Int. Symp. Circuits Syst. (ISCAS)*, Shanghai, China, May 2026, pp. 3391–3395, doi: 10.1109/ISCAS66217.2026.11562058.

[5] S. Kim and T. Kim, "CFET-FP: Complementary FET standard cell synthesis with optimal transistor folding and placement for design and technology co-optimization," *IEEE Trans. Comput.-Aided Design Integr. Circuits Syst.*, vol. 45, no. 10, pp. 4693–4706, Oct. 2026, doi: 10.1109/TCAD.2026.3654920.

[6] Embench, "Embench IoT benchmark suite," version 1.0, 2021. [Online]. Available: https://github.com/embench/embench-iot
