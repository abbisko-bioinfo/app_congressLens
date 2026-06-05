#!/bin/bash
# CongressLens — bulk import script via REST API
# Usage: ./scripts/import_all.sh [--data-root /data/attachmentFiles]
# Requires: backend running at API_HOST, curl, jq

set -euo pipefail

API_HOST="${API_HOST:-http://localhost:8050}"
DATA_ROOT="${DATA_ROOT:-/data/attachmentFiles}"

# Parse --data-root override
while [[ $# -gt 0 ]]; do
    case "$1" in
        --data-root) DATA_ROOT="$2"; shift 2 ;;
        --api-host)  API_HOST="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $*"; }
err()  { echo -e "${RED}[$(date +%H:%M:%S)] ERROR:${NC} $*"; }
step() { echo -e "\n${CYAN}=== $* ===${NC}"; }

api_post() {
    # POST to API, return JSON. Usage: api_post /path "key=val&key2=val2"
    local path="$1"
    local params="$2"
    curl -sS --max-time 600 -X POST "${API_HOST}/api${path}?${params}"
}

# ── Step 1: Create conferences ──────────────────────────────────────
step "Step 1: Creating conference records"

create_conference() {
    # We use the importer endpoints — they need existing conferences
    # Check if conference exists, create if not via direct SQL...
    # For simplicity, conferences are created by the import script in backend
    log "Conferences should already exist in DB (use scripts/import_conferences.py)"
    log "Checking API health..."
    curl -sS "${API_HOST}/health" > /dev/null || { err "Backend not reachable at $API_HOST"; exit 1; }
    log "API health OK"
}

create_conference

# ── Step 2: Get conference IDs ──────────────────────────────────────
step "Step 2: Getting conference IDs"

CONF_JSON=$(curl -sS "${API_HOST}/api/conferences?limit=10")
AACR25_ID=$(echo "$CONF_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(i['id']) for i in d.get('items',[]) if i['acronym']=='AACR' and i['year']==2025]" 2>/dev/null || echo "")
AACR26_ID=$(echo "$CONF_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(i['id']) for i in d.get('items',[]) if i['acronym']=='AACR' and i['year']==2026]" 2>/dev/null || echo "")
ASCO26_ID=$(echo "$CONF_JSON" | python3 -c "import json,sys; d=json.load(sys.stdin); [print(i['id']) for i in d.get('items',[]) if i['acronym']=='ASCO' and i['year']==2026]" 2>/dev/null || echo "")

if [ -z "$AACR25_ID" ] || [ -z "$AACR26_ID" ] || [ -z "$ASCO26_ID" ]; then
    err "Conference records not found. Run the import script first:"
    err "  docker compose exec backend python -m scripts.import_conferences --data-root $DATA_ROOT"
    exit 1
fi

log "AACR-2025: $AACR25_ID"
log "AACR-2026: $AACR26_ID"
log "ASCO-2026: $ASCO26_ID"

# ── Step 3: Import AACR-2025 sessions ───────────────────────────────
step "Step 3: Importing AACR-2025 sessions (652 files)"

log "POST /api/import/conferences/{id}/sessions?source=aacr&folder_path=$DATA_ROOT/AACR-2025"
RESULT=$(api_post "/import/conferences/${AACR25_ID}/sessions" \
    "source=aacr&folder_path=${DATA_ROOT}/AACR-2025")
echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  Sessions imported: {d.get(\"imported_sessions\",0)}')
print(f'  Skipped: {d.get(\"skipped\",0)}')
errors = d.get('errors',[])
if errors:
    print(f'  Errors: {len(errors)} (first: {errors[0][:120]})')
" 2>/dev/null || log "(check above for result)"

# ── Step 4: Import AACR-2026 sessions ───────────────────────────────
step "Step 4: Importing AACR-2026 sessions (635 files)"

log "POST /api/import/conferences/{id}/sessions?source=aacr&folder_path=$DATA_ROOT/AACR-2026"
RESULT=$(api_post "/import/conferences/${AACR26_ID}/sessions" \
    "source=aacr&folder_path=${DATA_ROOT}/AACR-2026")
echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  Sessions imported: {d.get(\"imported_sessions\",0)}')
print(f'  Skipped: {d.get(\"skipped\",0)}')
" 2>/dev/null || log "(check above for result)"

# ── Step 5: Import AACR-2025 presentations ──────────────────────────
step "Step 5: Importing AACR-2025 presentations (9,107 files)"

log "POST /api/import/conferences/{id}/presentations?source=aacr&folder_path=$DATA_ROOT/AACR-2025"
RESULT=$(api_post "/import/conferences/${AACR25_ID}/presentations" \
    "source=aacr&folder_path=${DATA_ROOT}/AACR-2025")
echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  Presentations: {d.get(\"imported_presentations\",0)}')
print(f'  Authors: {d.get(\"imported_authors\",0)}')
print(f'  Sessions: {d.get(\"imported_sessions\",0)}')
print(f'  Skipped: {d.get(\"skipped\",0)}')
errors = d.get('errors',[])
print(f'  Errors: {len(errors)}')
if errors:
    for e in errors[:3]: print(f'    - {e[:150]}')
    if len(errors) > 3: print(f'    ... and {len(errors)-3} more')
" 2>/dev/null || log "(check above for result)"

# ── Step 6: Import AACR-2026 presentations ──────────────────────────
step "Step 6: Importing AACR-2026 presentations (9,644 files)"

log "POST /api/import/conferences/{id}/presentations?source=aacr&folder_path=$DATA_ROOT/AACR-2026"
RESULT=$(api_post "/import/conferences/${AACR26_ID}/presentations" \
    "source=aacr&folder_path=${DATA_ROOT}/AACR-2026")
echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  Presentations: {d.get(\"imported_presentations\",0)}')
print(f'  Authors: {d.get(\"imported_authors\",0)}')
print(f'  Skipped: {d.get(\"skipped\",0)}')
errors = d.get('errors',[])
print(f'  Errors: {len(errors)}')
if errors:
    for e in errors[:3]: print(f'    - {e[:150]}')
" 2>/dev/null || log "(check above for result)"

# ── Step 7: Import ASCO-2026 presentations ──────────────────────────
step "Step 7: Importing ASCO-2026 presentations (7,293 files)"

log "POST /api/import/conferences/{id}/presentations?source=asco&folder_path=$DATA_ROOT/ASCO-2026"
RESULT=$(api_post "/import/conferences/${ASCO26_ID}/presentations" \
    "source=asco&folder_path=${DATA_ROOT}/ASCO-2026")
echo "$RESULT" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'  Presentations: {d.get(\"imported_presentations\",0)}')
print(f'  Authors: {d.get(\"imported_authors\",0)}')
print(f'  Sessions: {d.get(\"imported_sessions\",0)}')
print(f'  Skipped: {d.get(\"skipped\",0)}')
errors = d.get('errors',[])
print(f'  Errors: {len(errors)}')
if errors:
    for e in errors[:3]: print(f'    - {e[:150]}')
" 2>/dev/null || log "(check above for result)"

# ── Step 8: Verification ────────────────────────────────────────────
step "Step 8: Final verification"

echo "Conference | Year | Sessions | Presentations | Authors"
echo "-----------|------|----------|---------------|--------"
curl -sS "${API_HOST}/api/conferences?limit=10" | python3 -c "
import json,sys
data = json.load(sys.stdin)
for c in data.get('items',[]):
    sessions = c.get('session_count','?')
    pres = c.get('presentation_count','?')
    print(f'{c[\"acronym\"]:11} | {c[\"year\"]} | {sessions:>8} | {pres:>13} | N/A')
" 2>/dev/null

echo ""
log "Import complete! Check http://localhost:8051 for the frontend."