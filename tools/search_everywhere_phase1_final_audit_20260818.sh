#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

bash tools/build_cloudflare.sh

run_audit() {
  local title="$1"
  local script="$2"
  echo
  echo "===== ${title} ====="
  python3 "$script"
}

run_audit "AUDIT TRASVERSALE" tools/search_everywhere_cluster_audit_20260818.py
run_audit "INTENTI AD ALTA INTENZIONE" tools/search_everywhere_growth_gap_audit_20260818.py
run_audit "RESTYLING" tools/search_everywhere_restyling_gap_audit_20260818.py
run_audit "PRE-CANTIERE" tools/search_everywhere_pre_cantiere_gap_audit_20260818.py
run_audit "ILLUMINAZIONE" tools/search_everywhere_lighting_gap_audit_20260818.py
run_audit "PIANO DI LAVORO" tools/search_everywhere_worktop_gap_audit_20260818.py
run_audit "VINCOLI VERTICALI" tools/search_everywhere_vertical_constraints_gap_audit_20260818.py
run_audit "POSIZIONE LAVASTOVIGLIE" tools/search_everywhere_dishwasher_position_gap_audit_20260818.py
run_audit "CAPPA / INDUZIONE / ANTICONDENSA" tools/search_everywhere_hood_induction_decision_gap_audit_20260818.py
run_audit "PACCHETTO ELETTRODOMESTICI" tools/search_everywhere_appliance_package_gap_audit_20260818.py
run_audit "FRIGORIFERO" tools/search_everywhere_fridge_installation_gap_audit_20260818.py
run_audit "SCELTA LAVELLO" tools/search_everywhere_sink_choice_gap_audit_20260818.py
run_audit "ASPIRAZIONE INTEGRATA" tools/search_everywhere_integrated_extractor_gap_audit_20260818.py

echo
echo "===== STATO GIT ====="
git status --short

echo
echo "Audit master finale fase 1 Search Everywhere completato."
