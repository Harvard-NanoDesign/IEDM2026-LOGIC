# Copyright (c) 2026 Harvard University
# SPDX-License-Identifier: MIT
"""Shared helpers for the public carbon scripts: read the flows and configs, write result tables."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
FLOWS_DIR = HERE / "carbon_embodied" / "process_flows"
CARBON_DIR = HERE / "carbon_embodied" / "carbon_configuration"
OUTPUTS = HERE / "outputs"
FLOWS = ["FF", "NSH", "sCF", "mCF"]
CATEGORIES = ["Dry_etch", "Metallization", "Wet_etch", "Deposition",
              "EUV", "ArFi_LE", "ArF_LE", "KrF", "HG"]


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def read_config(name: str) -> dict:
    """Read carbon_embodied/carbon_configuration/<name>: nested `key: value` YAML mappings (no lists), without PyYAML."""
    root: dict = {}
    stack = [(-1, root)]
    for raw in (CARBON_DIR / name).read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        if line.lstrip().startswith("-") or ":" not in line:
            raise ValueError(f"{name}: unsupported YAML (only nested `key: value` mappings): {raw!r}")
        key, _, value = line.strip().partition(":")
        while indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value.strip():
            text = value.strip()
            try:
                parent[key] = float(text)
            except ValueError:
                parent[key] = text.strip("\"'")
        else:
            parent[key] = {}
            stack.append((indent, parent[key]))
    return root


def read_flow(flow: str) -> list[dict]:
    return read_csv(FLOWS_DIR / f"{flow}_detailed_flow.csv")


def totals(field: str) -> dict[str, Counter]:
    """Sum a numeric flow column by (FEOL/BEOL, Category) for every flow."""
    result = {}
    for flow in FLOWS:
        result[flow] = Counter()
        for row in read_flow(flow):
            result[flow][(row["FEOL/BEOL"], row["Category"])] += float(row[field] or 0)
    return result


def combined(steps: dict[str, Counter]) -> dict[str, Counter]:
    """Collapse (FEOL/BEOL, Category) totals from `totals` to FEOL + BEOL per Category."""
    result = {}
    for flow, counts in steps.items():
        result[flow] = Counter()
        for (section, category), value in counts.items():
            if section in ("FEOL", "BEOL"):
                result[flow][category] += value
    return result


def write_table(name: str, header: list[str], rows: list[list]):
    """Write outputs/<name> with one column per flow."""
    OUTPUTS.mkdir(exist_ok=True)
    path = OUTPUTS / name
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow([*header, *FLOWS])
        for row in rows:
            writer.writerow([value if isinstance(value, str) else f"{value:.10g}" for value in row])
    print(f"Wrote {path.relative_to(HERE)}")
