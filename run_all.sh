#!/usr/bin/env bash
# Regenerate every table in outputs/ from the process flows and configurations.
set -euo pipefail
cd "$(dirname "$0")"
for script in count_steps.py epw.py gpw.py mpw.py; do
    echo "== $script"
    python3 "$script"
done
