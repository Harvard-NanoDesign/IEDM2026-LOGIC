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
| `technologies/logic/` | The process flows of the four technologies: `ff` (FF, with an EUV front end; see [Updates since the IEDM 2026 paper](#updates-since-the-iedm-2026-paper)), `nsh` (NSH), `scfet` (sCF), and `mcfet` (mCF). Each folder holds the process flow CSV (`<tech>_final.csv`, one row per process step with its process area), a layout `.gds` for the 3D process simulation, and a `tech.yaml`. |
| `config/` | `carbon_config.yaml` (tool energy, input gases, and gas emissions per process area) and `materials.yaml` (density and GWP of each material, wafer size, yield): the CarbonEDA configuration the outputs were computed with. |
| `outputs/logic/<tech>/carbon/` | The CarbonEDA carbon results of each technology: `steps.csv` (EPW, MPW, and GPW per process step), `gases.csv` (per gas and step), `by_module.csv`, `by_area.csv`, and `totals.csv`. |
| `outputs/logic/<tech>/report/` | `<tech>_design_review.pdf`: the design review of each technology, with one page per process step showing its 3D structure from the SPX simulation, cross-sections, mask, materials, and EPW, MPW, and GPW, plus summaries by module and process area. |
| `summary/` | The technologies side by side: `totals.csv` (step counts, energy, EPW, MPW, GPW, and total per wafer), `process_steps.csv` and `epw.csv` (step counts and EPW per process area), `mpw.csv` (wafers, deposited materials, and upstream production of each input gas), and `gpw.csv` (each gas emitted after abatement). EPW includes the 40% facility overhead. |
| `power_performance_area_total_carbon/` | `PPAtC.csv`: power, performance, area, and total carbon for every ARM Cortex-M0 physical design. |
| `summarize.py` | Builds `summary/` from `outputs/` and updates the C<sub>embodied</sub> columns of `PPAtC.csv`. |

## Embodied carbon

C<sub>embodied</sub> per wafer is EPW + MPW + GPW, in kgCO<sub>2</sub>e per 300 mm wafer before yield:

| | FF | NSH | sCF | mCF |
| --- | --- | --- | --- | --- |
| Process step count | 574 | 840 | 933 | 859 |
| EPW with 40% fab overhead | 337.98 | 498.48 | 557.47 | 506.44 |
| MPW | 38.34 | 68.29 | 96.37 | 67.62 |
| GPW | 121.79 | 168.54 | 193.43 | 169.02 |
| **C<sub>embodied</sub> per wafer** | **498.11** | **735.30** | **847.27** | **743.09** |

The process steps exclude the starting, donor, and carrier wafers and the bond and flip steps; their wafers are still counted in MPW.

### Updates since the IEDM 2026 paper

Since the IEDM 2026 paper, we have improved the process flows and carbon footprint modeling:

- **More detailed process areas.** Process areas now distinguish wafer cleans, resist steps, and CMP (`Wafer_clean`, `Resist`, and `CMP`) and anneals and implants (`Diffusion` and `Ion_implantation`).
- **Byproduct gases in GPW.** We updated the GPW calculation to use total input gas to calculate the fraction of gas that leads to byproducts, in constrast to unutilized gas.
- **FF process flow improvements:** Source/drain contacts use single EUV exposures rather than multipatterning.
- **sCF/mCF process flow improvements:** Improved connectivity between two FET tiers with top and bottom gate/via cut steps.

The tables below compare each fab process as published in the paper with the updated flows as of 11/1/2026.

| FF |  |  |  |  |  |
| :---- | :---- | :---- | :---- | :---- | :---- |
|  | **Total embodied carbon per wafer (kgCO<sub>2</sub>e)** | **EPW with 40% fab overhead (kgCO<sub>2</sub>e/wafer)** | **MPW (kgCO<sub>2</sub>e/wafer)** | **GPW (kgCO<sub>2</sub>e/wafer)** | **Process step count** |
| **IEDM ‘26** | 504.28 | 350.19 | 41.57 | 112.52 | 601 |
| **11/1/2026** | 498.11 | 337.98 | 38.34 | 121.79 | 574 |
| **Percent Change (%)** | \-1.2 | \-3.5 | \-7.8 | 8.2 | \-4.5 |

| NSH |  |  |  |  |  |
| :---- | :---- | :---- | :---- | :---- | :---- |
|  | **Total embodied carbon per wafer (kgCO<sub>2</sub>e)** | **EPW with 40% fab overhead (kgCO<sub>2</sub>e/wafer)** | **MPW (kgCO<sub>2</sub>e/wafer)** | **GPW (kgCO<sub>2</sub>e/wafer)** | **Process step count** |
| **IEDM ‘26** | 712.35 | 496.40 | 71.76 | 144.19 | 849 |
| **11/1/2026** | 735.30 | 498.48 | 68.29 | 168.54 | 840 |
| **Percent Change (%)** | 3.2 | 0.4 | \-4.8 | 16.9 | \-1.1 |

| sCF |  |  |  |  |  |
| :---- | :---- | :---- | :---- | :---- | :---- |
|  | **Total embodied carbon per wafer (kgCO<sub>2</sub>e)** | **EPW with 40% fab overhead (kgCO<sub>2</sub>e/wafer)** | **MPW (kgCO<sub>2</sub>e/wafer)** | **GPW (kgCO<sub>2</sub>e/wafer)** | **Process step count** |
| **IEDM ‘26** | 816.11 | 547.22 | 100.79 | 168.10 | 926 |
| **11/1/2026** | 847.27 | 557.47 | 96.37 | 193.43 | 933 |
| **Percent Change (%)** | 3.8 | 1.9 | \-4.4 | 15.1 | 0.8 |

| mCF |  |  |  |  |  |
| :---- | :---- | :---- | :---- | :---- | :---- |
|  | **Total embodied carbon per wafer (kgCO<sub>2</sub>e)** | **EPW with 40% fab overhead (kgCO<sub>2</sub>e/wafer)** | **MPW (kgCO<sub>2</sub>e/wafer)** | **GPW (kgCO<sub>2</sub>e/wafer)** | **Process step count** |
| **IEDM ‘26** | 702.77 | 486.77 | 71.37 | 144.64 | 838 |
| **11/1/2026** | 743.09 | 506.44 | 67.62 | 169.02 | 859 |
| **Percent Change (%)** | 5.7 | 4.0 | \-5.3 | 16.9 | 2.5 |

`power_performance_area_total_carbon/PPAtC.csv` uses the updated values (11/1/2026).

## Reproducing the results

The carbon results are computed with [CarbonEDA](https://github.com/Harvard-NanoDesign/CarbonEDA) v0 (commit `310762a`). The carbon CSVs need only Python 3.9 or later:

```bash
git clone https://github.com/Harvard-NanoDesign/CarbonEDA.git
cd CarbonEDA && git checkout 310762a && make venv
cp -r /path/to/IEDM2026-LOGIC/technologies/logic technologies/
cp /path/to/IEDM2026-LOGIC/config/*.yaml config/
for t in ff nsh scfet mcfet; do make carbon TECH=logic/$t; done
```

This writes `outputs/logic/<tech>/carbon/`, which matches `outputs/logic/` here. To change an assumption, such as the fab carbon intensity or the facility overhead, edit `config/carbon_config.yaml` and rerun `make carbon`. Then copy the new `outputs/logic/` here and run `python3 summarize.py` (standard library only) to rebuild `summary/` and `PPAtC.csv`.

With Synopsys Sentaurus Process Explorer (SPX) and Sentaurus Visual installed, `make all TECH=logic/<tech>` also runs the 3D process simulation of each flow on its layout and regenerates the design-review PDFs in `outputs/logic/<tech>/report/`. See the CarbonEDA README for the setup.

## Citation

D. Kong, D. Grey-Stewart, M. Elgamal, Z. Chen, Z. Piao, J. Morris, Y. Yao, and G. Hills, “Quantifying Trade-Offs in Power, Performance, Area, and Total Carbon Footprint (PPAtC) of Next Directions in FET Technologies for VLSI Digital Logic Circuits,” *2026 IEEE International Electron Devices Meeting (IEDM)*, San Francisco, CA, USA, 2026, pp. 1-4.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
