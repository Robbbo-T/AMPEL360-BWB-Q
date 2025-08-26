#!/usr/bin/env bash
# .git/hooks/pre-commit
set -euo pipefail

CHANGED=$(git diff --cached --name-only --diff-filter=ACM | grep -E "UTCS-[0-9]{2}-" || true)
if [ -n "$CHANGED" ]; then
    echo "Updating ledger-plan.json for UTCS artifacts..."
    python T-TECHNOLOGICAL/LEDGER/cli/make_plan.py $CHANGED
    git add T-TECHNOLOGICAL/LEDGER/cli/ledger-plan.json
fi
