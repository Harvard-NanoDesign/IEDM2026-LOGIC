# Technologies

The [CarbonEDA](https://github.com/Harvard-NanoDesign/CarbonEDA) technology inputs for the four FET technologies. Copy `logic/` into CarbonEDA's `technologies/` folder to run them (see [Reproducing the results](../README.md#reproducing-the-results)).

| Folder | Technology |
| --- | --- |
| `logic/ff/` | FinFET (FF), 7 nm class, FEOL through M9, with an EUV front end: Samsung 4LPE-class STI, gate, replacement metal gate, and single-EUV-exposure contacts, with the paper's FF BEOL (see [Updates since the IEDM 2026 paper](../README.md#updates-since-the-iedm-2026-paper)) |
| `logic/nsh/` | Nanosheet FET (NSH), 2 nm class, with a backside power network on a bonded carrier wafer; each BEOL tier M*n* uses the GT2 via under its metal (V*n*−1) |
| `logic/scfet/` | Sequential CFET (sCF), NMOS bottom tier and PMOS top tier, on 2 nm nanosheet rules (CPP 42) with the NSH BEOL: the top tier is bonded from a donor wafer, and the backside is built on a bonded carrier wafer |
| `logic/mcfet/` | Monolithic CFET (mCF), NMOS bottom tier and PMOS top tier, on the same layout and BEOL as sCF, with the backside on a bonded carrier wafer |

Each folder holds three files:

| File | Contents |
| --- | --- |
| `<tech>_final.csv` | The process flow, one row per module header (`row_type` = `module`) or process step (`row_type` = `step`). `module`, `step`, and `step_type` name the step, and `carboneda_process_area` is the process area that sets its tool energy and gases in `../config/carbon_config.yaml`. The remaining columns (`MaterialFilter`, `Thickness`, `Rate`, `Time`, `BondTopStep`, `Flip`, …) are the Sentaurus Process Explorer (SPX) parameters of the step and the deposited thickness and materials used for MPW. In `scfet_final.csv`, the `route` column marks the rows that prepare the donor wafer for the top tier (`Seq_Top_Wafer`). |
| `<tech>_layout.gds` | The layout for the SPX 3D process simulation. For `nsh`, the GT2 nanosheet flip-flop cell with a generated BEOL test pattern. For `scfet` and `mcfet`, a 4-track (96 nm) CFET flip-flop cell (DFFHQNx1) routed on its own M0 to M2 to the GT2 rules, with the NSH BEOL above it, in GT2 layer numbers with the tier as the datatype (0 shared, 1 bottom, 2 top). For `ff`, a generated test pattern. |
| `tech.yaml` | The CarbonEDA settings for the technology: the flow CSV and layout, the carrier-wafer routes, the simulation clip, and the cut planes for the design-review renders. |

The carbon results computed from these flows are in `../outputs/logic/<tech>/`.
