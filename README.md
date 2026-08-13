# IEDM2026-LOGIC

## Summary

Computing's *carbon footprint* has become a major consideration when designing future generations of VLSI circuits, accounting for both *embodied carbon* (C<sub>embodied</sub>) due to Integrated Circuit (IC) fabrication, and *operational carbon* (C<sub>operational</sub>) due to day-to-day use. In this paper, we quantify *trade-offs* in power, performance, area, and total carbon footprint (tC = C<sub>embodied</sub> + C<sub>operational</sub>, in kilograms of CO<sub>2</sub> equivalent) of next directions in FET technologies for high performance digital VLSI logic circuits. Specifically, we analyze the impact of advancing from today's FinFETs (FF) to each of *3* types of gate-all-around FETs:
(1) Nanosheet (NSH) FETs;
(2) *Sequential* Complementary FETs (*s*CF), in which NMOS & PMOS NSHFETs are fabricated on separate substrates that are subsequently bonded together; and
(3) *Monolithic* Complementary FETs (*m*CF), in which NMOS & PMOS NSHFETs are fabricated on the same starting substrate.

We develop detailed models to quantify C<sub>embodied</sub> for each direction, accounting for energy, material, and gas use from more than 500 individual process steps in complete fabrication processes. We then leverage industry-standard VLSI design flows to create full physical designs of a processor core (ARM Cortex-M0) using each FET technology and quantify power, performance, area, and C<sub>operational</sub> allowing us to optimize overall tCDP.

## Data

The `data/` directory contains `epw.csv`, `mpw.csv`, `gpw.csv`, and `process_steps.csv`, which provide the energy-per-wafer emissions, material-per-wafer emissions, gas-per-wafer emissions, and fabrication process-step counts, respectively, for FF, NSH, sCF, and mCF technologies.

## Citation

D. Kong, D. Grey-Stewart, M. Elgamal, Z. Chen, Z. Piao, J. Morris, Y. Yao, and G. Hills, “Quantifying Trade-Offs in Power, Performance, Area, and Total Carbon Footprint (PPAtC) of Next Directions in FET Technologies for VLSI Digital Logic Circuits,” *2026 IEEE International Electron Devices Meeting (IEDM)*, San Francisco, CA, USA, 2026, pp. 1-4.
