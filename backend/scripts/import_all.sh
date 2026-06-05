#!/bin/bash
# CongressLens — batched import via REST API
# Each call imports at most BATCH_SIZE files to avoid timeouts
set -euo pipefail

API="${API_HOST:-http://localhost:8050}"
DATA="${DATA_ROOT:-/data/attachmentFiles}"
BATCH="${BATCH_SIZE:-2000}"  # files per API call

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; NC='\033[0m'
log()  { echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $*"; }
warn() { echo -e "${RED}[$(date +%H:%M:%S)]${NC} $*"; }

api() {
    # $1=path $2=params  →  outputs JSON
    curl -sS --max-time 300 -X POST "${API}/api${1}?${2}"
}

# ── Resolve conference IDs ──────────────────────────────────────────
CONF_JSON=$(curl -sS "${API}/api/conferences?limit=10")

cid() { echo "$CONF_JSON" | python3 -c "
import json,sys
d=json.load(sys.stdin)
[print(i['id']) for i in d.get('items',[]) if i['acronym']=='$1' and i['year']==$2]" 2>/dev/null; }

A25=$(cid AACR 2025); A26=$(cid AACR 2026); S26=$(cid ASCO 2026)
if [[ -z "$A25" || -z "$A26" || -z "$S26" ]]; then
    warn "Conferences not found. Run: docker compose exec backend python -m scripts.import_conferences --data-root $DATA"
    exit 1
fi
log "AACR-2025=$A25  AACR-2026=$A26  ASCO-2026=$S26"

# ── Helper: batch import ───────────────────────────────────────────
batch_import() {
    local label="$1" endpoint="$2" cid="$3" source="$4" folder="$5" total="$6"
    log "Importing $label ($total files, batch=$BATCH)..."
    local offset=0
    while true; do
        local result
        result=$(api "$endpoint" "source=${source}&folder_path=${DATA}/${folder}&max_files=${BATCH}")
        local pres=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('imported_presentations',0))" 2>/dev/null || echo 0)
        local sess=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('imported_sessions',0))" 2>/dev/null || echo 0)
        local auth=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('imported_authors',0))" 2>/dev/null || echo 0)
        local skip=$(echo "$result" | python3 -c "import json,sys; print(json.load(sys.stdin).get('skipped',0))" 2>/dev/null || echo 0)
        local total_imported=$((pres + sess))
        offset=$((offset + BATCH))
        log "  batch ~${offset}: P=$pres S=$sess A=$auth skip=$skip"
        # Stop when no new records imported this batch
        if [[ "$total_imported" -eq 0 ]]; then
            log "  ✓ $label complete (no more records)"
            break
        fi
    done
}

# ── Import order ─────────────────────────────────────────────────────

# 1. AACR sessions (small, one batch is fine)
log "=== AACR-2025 sessions ==="
api "/import/conferences/${A25}/sessions" "source=aacr&folder_path=${DATA}/AACR-2025&max_files=1000" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  S={d.get(\"imported_sessions\",0)} skip={d.get(\"skipped\",0)}')"

log "=== AACR-2026 sessions ==="
api "/import/conferences/${A26}/sessions" "source=aacr&folder_path=${DATA}/AACR-2026&max_files=1000" \
    | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  S={d.get(\"imported_sessions\",0)} skip={d.get(\"skipped\",0)}')"

# 2. AACR presentations
batch_import "AACR-2025 pres" "/import/conferences/${A25}/presentations" "$A25" "aacr" "AACR-2025" 9107
batch_import "AACR-2026 pres" "/import/conferences/${A26}/presentations" "$A26" "aacr" "AACR-2026" 9644

# 3. ASCO presentations
batch_import "ASCO-2026 pres"  "/import/conferences/${S26}/presentations" "$S26" "asco" "ASCO-2026" 7293

log "=== All imports complete ==="