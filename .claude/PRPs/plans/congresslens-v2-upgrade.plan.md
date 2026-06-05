# Plan: CongressLens v2 Upgrade — Frontend Replication + Data Ingestion + LDAP Auth

## Summary
Upgrade CongressLens from prototype MVP to production-ready v2: 100% replicate the demo HTML (`congress_lens_modified_v4.html`) visual design and page structure, ingest real AACR/ASCO conference data from JSON files into the database, and add LDAP-based user authentication with admin controls and anonymous browsing.

## User Story
As an oncology researcher, I want a professional conference intelligence workspace that displays real session/presentation data with polished UI, so that I can browse conferences anonymously and star/edit content after LDAP login.

## Problem → Solution
**Current**: Generic gray MVP pages, no real data, no authentication — reads as a prototype.  
**Desired**: Polished design-system-driven pages with real AACR-2025/2026 + ASCO-2026 data, LDAP auth with anonymous browse and authenticated edit/star.

## Metadata
- **Complexity**: XL (3 major subsystems: frontend rewrite, data pipeline, auth system)
- **Source PRD**: N/A
- **PRD Phase**: N/A
- **Estimated Files**: ~35

---

## UX Design

### Before
```
┌──────────────────────────────────────────────────┐
│  Sidebar (gray, generic)  │  Dashboard (gray)   │
│  - Dashboard              │  - Watchlist table   │
│  - Conferences            │  - Recent conferences│
│  - Presentations          │  - AI placeholder    │
│  - Calendar               │  - No auth context   │
│                           │  - No real data       │
└──────────────────────────────────────────────────┘
```

### After
```
┌──────────────────────────────────────────────────────────────┐
│  Header (sticky, blue/white, Material Symbols icons)        │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ Congress Lens  | Sessions | Presentations | Star | 🔍⚙️ │ │
│  │                    Dr. Aris Thorne (LDAP user)          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Dashboard: Conference cards + Calendar grid                 │
│  Sessions: Accordion-style expandable rows                   │
│  Presentations: Table with Star/Type/Title/Presenter/Topic   │
│  Star Page: Bookmarked presentations across conferences      │
│  Footer: Congress Lens © 2026                                │
└──────────────────────────────────────────────────────────────┘
```

### Interaction Changes
| Touchpoint | Before | After | Notes |
|---|---|---|---|
| Navigation | Sidebar (always visible) | Top header sticky bar | Demo uses sticky header with congress dropdown |
| Congress select | Click conference card | URL-based `/session/:congress` + dropdown selector | URL-driven state per demo |
| Dashboard | Static lists | Calendar grid + conference cards | Demo uses 5-day grid |
| Sessions page | Simple list | Accordion expandable rows with embedded presentation table | Demo pattern |
| Presentations | Plain table | Rich table with Star/Type badge/Topic/Files count/Detail link | Demo pattern |
| Auth | None | Anonymous browse + LDAP login for edit/star | New |
| Star/Watchlist | Requires login (API fails without user_id) | Anonymous can browse; star requires auth | Permission change |

---

## Mandatory Reading

| Priority | File | Lines | Why |
|---|---|---|---|
| P0 | `demo/congress_lens_modified_v4.html` | 1-404 | **100% replication target** — all page structures, color tokens, component patterns |
| P0 | `design.md` | 1-401 | Design system tokens — colors, typography, spacing, radius, components |
| P0 | `attachmentFiles/AACR-2026/AACR-2026.ipynb` | all | AACR notebook — JSON download + merge + session/presentation parsing + AdditionalFields flattening pattern |
| P0 | `backend/app/importers/aacr.py` | 1-143 | AACR importer pattern — how sessions/presentations are parsed from JSON |
| P0 | `backend/app/importers/asco.py` | 1-180 | ASCO importer pattern — nested GraphQL-style data extraction |
| P1 | `frontend/src/api/client.ts` | 1-209 | API client — all endpoints, types, fetch patterns |
| P1 | `backend/app/models/presentation.py` | 1-87 | Presentation model — all columns, relationships, indexes |
| P1 | `backend/app/models/session.py` | 1-38 | Session model — columns, relationships |
| P1 | `backend/app/models/conference.py` | 1-29 | Conference model — columns, unique constraint |
| P1 | `backend/app/models/watchlist_item.py` | 1-28 | Watchlist model — user_id nullable, target types |
| P2 | `frontend/src/pages/Dashboard.tsx` | 1-100 | Current dashboard — what gets replaced |
| P2 | `frontend/src/components/Layout.tsx` | 1-30 | Current layout — sidebar gets replaced by header |
| P2 | `backend/app/core/config.py` | 1-19 | Settings class — where LDAP config will be added |
| P2 | `backend/app/main.py` | 1-33 | FastAPI app — where auth middleware will be added |
| P2 | `frontend/package.json` | 1-35 | Dependencies — Material Symbols font needed |

## External Documentation

| Topic | Source | Key Takeaway |
|---|---|---|
| LDAP auth in Python | `python-ldap` / `ldap3` library docs | Use `ldap3` (async-friendly, pure Python); bind with DN template `%s@company.com` |
| LDAP auth in FastAPI | FastAPI security docs | Use `Depends()` with custom `get_current_user` that checks LDAP session cookie |
| Material Symbols | Google Fonts CDN | `<link href="...Material+Symbols+Outlined..." />` — FILL/wght/GRAD/opsz variants |
| Tailwind v4 | Tailwind CSS v4 docs | `@import "tailwindcss"` + `@theme` block for custom tokens in CSS |

---

## Patterns to Mirror

### NAMING_CONVENTION
// SOURCE: `frontend/src/api/client.ts:1-209`
```typescript
// TypeScript interfaces: PascalCase (Conference, Session, Presentation)
// API methods: camelCase nested objects (api.conferences.list, api.presentations.get)
// Route params: snake_case in API response (conference_id, session_id, presenter_name)
```

### ERROR_HANDLING
// SOURCE: `frontend/src/api/client.ts:145-154`
```typescript
async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, init);
  if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`);
  return res.json();
}
```

### REPOSITORY_PATTERN
// SOURCE: `backend/app/api/importer.py:1-22`
```python
# Importer uses Depends(get_db) for AsyncSession injection
# BaseImporter class pattern from app/importers/base.py
# Importer registry: IMPORTERS dict mapping source name to class
```

### SERVICE_PATTERN
// SOURCE: `backend/app/api/presentations.py` (existing pattern)
```python
# Router = APIRouter(prefix="/presentations", tags=["presentations"])
# Each endpoint uses Depends(get_db) for database session
# Returns SQLAlchemy model data as dict via Pydantic response model
```

### AUTH_PATTERN (NEW — to be established)
```python
# get_current_user: Depends on optional cookie/session token
# Returns User object or None (anonymous)
# Admin check: separate Depends(get_admin_user) that requires admin role
```

### TEST_STRUCTURE
// SOURCE: `backend/tests/` (if exists)
```python
# pytest with asyncio_mode = "auto" (from pyproject.toml)
# Test paths: ["tests"]
```

---

## Files to Change

| File | Action | Justification |
|---|---|---|
| `frontend/src/index.css` | REWRITE | Replace `@import "tailwindcss"` with full design system tokens from design.md |
| `frontend/src/components/Layout.tsx` | REWRITE | Replace sidebar layout with sticky header + footer from demo |
| `frontend/src/pages/Dashboard.tsx` | REWRITE | 100% replicate demo Dashboard (conference cards + calendar grid) |
| `frontend/src/pages/SessionList.tsx` | CREATE | New sessions page per demo (accordion expandable rows) |
| `frontend/src/pages/PresentationList.tsx` | REWRITE | 100% replicate demo PresentationTable (rich table with star/badge) |
| `frontend/src/pages/PresentationDetail.tsx` | REWRITE | 100% replicate demo PresentationDetail (3-column layout) |
| `frontend/src/pages/StarPage.tsx` | CREATE | New star/watchlist page per demo StarPage |
| `frontend/src/main.tsx` | UPDATE | New routes matching demo: `/`, `/session/:congress`, `/presentations/:congress`, `/presentations/:congress/:id`, `/star` |
| `frontend/src/api/client.ts` | UPDATE | Add auth endpoints, update watchlist to use auth context |
| `frontend/src/hooks/useAuth.ts` | CREATE | Auth context hook (LDAP login state, anonymous detection) |
| `frontend/src/components/AuthProvider.tsx` | CREATE | Auth context provider wrapping app |
| `frontend/src/components/ConferenceBadge.tsx` | CREATE | Reusable badge component per demo |
| `frontend/src/components/PageShell.tsx` | CREATE | Reusable page shell with header + congress selector per demo |
| `frontend/src/components/PresentationTable.tsx` | CREATE | Reusable presentation table component per demo |
| `frontend/src/components/CalendarGrid.tsx` | CREATE | Reusable 5-day calendar grid component per demo |
| `frontend/src/components/Footer.tsx` | CREATE | Footer component per demo |
| `frontend/src/components/Header.tsx` | CREATE | Header component per demo |
| `frontend/index.html` | UPDATE | Add Material Symbols font link |
| `frontend/package.json` | UPDATE | No new npm deps needed (Material Symbols via CDN link) |
| `backend/app/core/config.py` | UPDATE | Add LDAP settings (ldap_server, ldap_bind_dn_template, ldap_search_base, admin_users list) |
| `backend/app/auth/__init__.py` | CREATE | Auth module |
| `backend/app/auth/ldap.py` | CREATE | LDAP authentication logic using ldap3 |
| `backend/app/auth/dependencies.py` | CREATE | FastAPI Depends for get_current_user / get_admin_user |
| `backend/app/auth/models.py` | CREATE | User model (id, display_name, email, role, is_admin) |
| `backend/app/auth/routes.py` | CREATE | Login/logout/session-check endpoints |
| `backend/app/main.py` | UPDATE | Add auth middleware, session cookie handling |
| `backend/app/api/__init__.py` | UPDATE | Add auth_router |
| `backend/app/api/interactions.py` | UPDATE | Require auth for star/edit operations, anonymous for browse |
| `backend/app/api/watchlist.py` | UPDATE | Require auth for add/remove, anonymous list returns empty |
| `backend/app/models/user.py` | CREATE | User model for internal admin mapping |
| `backend/pyproject.toml` | UPDATE | Add `ldap3>=2.9.1` dependency |
| `backend/alembic/versions/` | CREATE | New migration for user table |
| `backend/app/importers/aacr.py` | UPDATE | Handle session JSON separately (session/ folder has `_summary.json` format) |
| `backend/app/importers/asco.py` | UPDATE | Handle ASCO-2026 JSON format differences |
| `backend/app/api/importer.py` | UPDATE | Add session import endpoint + bulk import script |
| `.env` + `.env.example` | UPDATE | Add LDAP config variables |
| `docker-compose.yml` | UPDATE | Mount attachmentFiles volume for importer access |

## NOT Building

- AI summary generation (still placeholder)
- E2E tests (follow-up task)
- Dark mode toggle (not in demo)
- Search functionality beyond placeholder UI (demo shows search box but no backend)
- Notification system (demo shows icon but no backend)
- Settings page (demo shows icon but no content)
- ESMO-2025 data ingestion (not requested; only AACR-2025, AACR-2026, ASCO-2026)
- AACR-2024 data ingestion (not requested)
- Password-based local auth (LDAP only)
- Role-based access beyond admin/non-admin (no editor/reviewer roles)

---

## Step-by-Step Tasks

### Task 1: Design System — CSS Tokens + Font Setup
- **ACTION**: Replace `frontend/src/index.css` with full design system from `design.md`. Add Material Symbols font to `frontend/index.html`.
- **IMPLEMENT**: Define all CSS custom properties from design.md Section 11 in `@theme` block. Add `@import "tailwindcss"` at top. Add font link in `index.html` head.
- **MIRROR**: Demo HTML `<script id="tailwind-config">` block (lines 11-59) and `<style>` block (lines 61-85) for token names and values.
- **IMPORTS**: None (CSS + HTML only)
- **GOTCHA**: Tailwind v4 uses `@theme` block for custom tokens, not `tailwind.config.js`. Material Symbols font URL must include `FILL@100..700,0..1` parameter for filled star icons.
- **VALIDATE**: Open dev server, verify background color is `#F6F8FB`, headings are `#3B5BA2`, Material Symbols icons render in Layout header.

### Task 2: Header + Footer + PageShell Components
- **ACTION**: Create `Header.tsx`, `Footer.tsx`, `PageShell.tsx` components replicating demo exactly.
- **IMPLEMENT**: Header with sticky top, nav links (Sessions/Presentations/Star), search bar, user avatar. Footer with copyright. PageShell with congress selector dropdown + title/subtitle layout.
- **MIRROR**: Demo `Header` component (lines 147-187), `PageShell` (lines 281-292), footer (lines 391-395).
- **IMPORTS**: `react-router-dom` (Link, useLocation, useParams), Material Symbols icon spans.
- **GOTCHA**: Demo has typo `presetation` (not `presentation`) in routes — fix in our implementation to use correct spelling. Nav needs congress param from URL path.
- **VALIDATE**: Header stays sticky on scroll, nav highlights correct tab, congress selector works.

### Task 3: Dashboard Page Rewrite
- **ACTION**: Rewrite `Dashboard.tsx` to replicate demo Dashboard (conference cards + calendar grid).
- **IMPLEMENT**: Left panel: conference cards with date/name/badge/stats. Right panel: 5-day calendar grid with session/presentation hits. Action buttons (Import Congress, Refresh API).
- **MIRROR**: Demo `Dashboard` component (lines 191-279).
- **IMPORTS**: `api` from client.ts, `useState`, Material Symbols icons, `Link`.
- **GOTCHA**: Calendar grid uses CSS `grid-template-columns: 80px repeat(5, minmax(180px, 1fr))`. Demo data is hardcoded — our version must use API data. Conference selection state drives both panels.
- **VALIDATE**: Conference cards render from API, calendar grid shows sessions at correct time slots, clicking card updates selected conference.

### Task 4: Sessions Page (Accordion Pattern)
- **ACTION**: Create `SessionList.tsx` (rename route) with accordion expandable session rows containing embedded PresentationTable.
- **IMPLEMENT**: Each session row shows date/time/type badge/title/track/room/presentation count. Clicking expands to show embedded presentation table. Congress selector dropdown via PageShell.
- **MIRROR**: Demo `SessionsPage` (lines 354-375).
- **IMPORTS**: `useState`, `useEffect`, `useParams`, `useLocation`, `api`, `PresentationTable`, `PageShell`.
- **GOTCHA**: Demo uses `open` state per session ID from URL query param `?session=`. Our version needs to pass `congress` param to API to filter sessions by conference.
- **VALIDATE**: Sessions list filtered by selected congress, accordion expand/collapse works, embedded presentations table renders.

### Task 5: PresentationTable + PresentationList + PresentationDetail Rewrite
- **ACTION**: Create reusable `PresentationTable.tsx` component. Rewrite `PresentationList.tsx` and `PresentationDetail.tsx` to match demo exactly.
- **IMPLEMENT**: PresentationTable: Star icon, Time column, Type badge (magenta), Title+abstract preview, Presenter+org, Topic, Files count, Detail link button. PresentationDetail: 3-column layout with header (type badge, star, title, metadata grid), abstract section, intelligence notes, attachments sidebar, comments section.
- **MIRROR**: Demo `PresentationTable` (lines 294-317), `PresentationsPage` (lines 319-323), `PresentationDetail` (lines 325-352).
- **IMPORTS**: `api`, `Link`, Material Symbols, `useParams`.
- **GOTCHA**: Star icon must use `font-variation-settings: 'FILL' 1` for filled state, `'FILL' 0` for unfilled. Presentation detail needs back-link to list page. Type badge uses `bg-secondary/10 text-secondary` per demo.
- **VALIDATE**: Table renders with all columns, badges show presentation_type, star toggle works (requires auth), detail page shows full abstract and metadata.

### Task 6: Star/Watchlist Page
- **ACTION**: Create `StarPage.tsx` showing starred presentations across all conferences.
- **IMPLEMENT**: Uses PresentationTable with `showConference=true` flag. Shows conference column. Filter by watchlist items for current user.
- **MIRROR**: Demo `StarPage` (line 377).
- **IMPORTS**: `api.watchlist`, `PresentationTable`, `PageShell`.
- **GOTCHA**: Requires auth — if anonymous, show "Login to star presentations" message. Demo uses `presentations.filter(p => p.starred)` — our version uses `api.watchlist.list()` then maps to presentations.
- **VALIDATE**: Starred items display with conference badge, clicking star toggles watchlist entry.

### Task 7: Route Structure Update
- **ACTION**: Update `main.tsx` routes to match demo URL structure. Remove sidebar-based Layout, use header-based.
- **IMPLEMENT**: Routes: `/` → Dashboard, `/session/:congress` → SessionList, `/presentations/:congress` → PresentationList, `/presentations/:congress/:id` → PresentationDetail, `/star` → StarPage. Wrap in AuthProvider + QueryClientProvider.
- **MIRROR**: Demo `App` routes (lines 380-390).
- **IMPORTS**: `BrowserRouter`, `Routes`, `Route`, `AuthProvider`, `QueryClientProvider`.
- **GOTCHA**: Demo has `/presetation/` typo — we use `/presentations/`. Old routes (`/conferences`, `/sessions/:id`) need migration. Remove `Layout` sidebar component.
- **VALIDATE**: All routes render correct pages, header nav highlights match current route, congress param extracted from URL.

### Task 8: Data Ingestion — Session Importer Enhancement (AACR + ASCO)
- **ACTION**: Update AACR importer to handle session JSON files from `session/` folder separately with full metadata. Update ASCO importer to extract session records from embedded `sessionId/sessionTitle/sessionType` fields in each presentation JSON. Add session import endpoint.
- **IMPLEMENT**: 
  - **AACR session import**: Session JSON files (`{id}_summary.json`) have different structure from presentation JSON. Key fields: `Id` (string), `Title`, `Number` (e.g., "AT07"), `Date` ("2026-04-19"), `StartTime` ("13:00"), `EndTime` ("14:30"), `Location` (e.g., "Ballroom 6 A"), `Duration` (90, minutes), `Description` (HTML), `AdditionalFields` (list of `{Key, Value}` pairs — flatten into `SessionName`, `AACRTrackAll`, `Presentation Count`). Reference `attachmentFiles/AACR-2026/AACR-2026.ipynb` cells 22-27 for the flattening pattern: `item.update({f"AdditionalFields.{x['Key']}": x["Value"] for x in item["AdditionalFields"]})`. Use `AdditionalFields.SessionName` for `session_type`, `AdditionalFields.AACRTrackAll` for `track` (comma-separated). Create separate import method `import_sessions_folder` that only processes session JSON files.
  - **ASCO session extraction**: ASCO-2026 has NO separate session JSON files. Instead, each presentation JSON contains `sessionId` (e.g., 17086), `sessionTitle` ("Care Delivery/Models of Care"), `sessionType` ("Poster Session"), `primaryTrack` (dict with `track` and `trackId`). During presentation import, extract these to create/ensure Session records. This means ASCO sessions are derived from presentation data — collect unique `sessionId` values and create sessions with `session_type` from `sessionType`, `title` from `sessionTitle`, `track` from `primaryTrack.track`. ASCO-2026 `details/` directory contains paginated search results (731 files, `page-*.json`) with `data.search.result.hits` arrays — these can provide additional session metadata if needed but are NOT the primary source.
  - **Import order**: Sessions first, then presentations (presentations reference sessions by `session_id` / `sessionId`). Add `/import/conferences/{conference_id}/sessions` endpoint for AACR. ASCO sessions are auto-created during presentation import.
- **MIRROR**: Existing `AACRImporter._ensure_session` pattern — but now sessions have full data, not just title stub. AACR-2026 notebook cells 22-27 for `AdditionalFields` flattening. ASCO `ASCOImporter._ensure_session` pattern — already handles embedded session data, just needs richer metadata extraction.
- **IMPORTS**: `json`, `Path`, `Session` model, `Conference` model, `bleach` (for HTML description sanitization).
- **GOTCHA**: AACR-2025 session files use `{id}_summary.json` naming, AACR-2026 same format. AACR session `AdditionalFields` flattening pattern from notebook: `{f"AdditionalFields.{x['Key']}": x["Value"] for x in item["AdditionalFields"]}` — must parse `SessionName`, `AACRTrackAll`, `Presentation Count`. AACR `Date` is `"2026-04-19"` (ISO date), `StartTime`/`EndTime` are HH:MM strings like `"13:00"` — need to combine into full datetime. ASCO `sessionId` is integer (17086), not string — convert to string for `source_session_id`. ASCO-2026 `details/page-*.json` is search result pagination, not session detail — do NOT use as session source.
- **VALIDATE**: Import AACR-2025/2026 sessions with full metadata (room, start_time, end_time, description, session_type from AdditionalFields.SessionName, track from AdditionalFields.AACRTrackAll). Import ASCO-2026 sessions extracted from presentations. Verify all sessions have meaningful content, not stub records.

### Task 9: Data Ingestion — Presentation Importer Verification + ASCO Session Extraction
- **ACTION**: Verify and fix AACR/ASCO presentation importers handle all JSON formats correctly. Ensure ASCO importer extracts full session info from embedded fields.
- **IMPLEMENT**: AACR-2025 presentations are `{id}_summary.json` (flat format). AACR-2026 presentations are `{id}.json` (same flat format). Both have `AdditionalFields` as list of `{Key, Value}` pairs — need flattening per notebook pattern: `{f"AdditionalFields.{x['Key']}": x["Value"] for x in data["AdditionalFields"]}` to extract Topics, Keywords, etc. ASCO-2026 presentations are `{id}.json` (nested `data.getContentById.result` format). ASCO importer already handles nested format. ASCO presentations contain embedded session info: `sessionId`, `sessionTitle`, `sessionType`, `primaryTrack` — these must be extracted during import to create/update Session records with richer metadata. ASCO `authors` use `ascoId`, `displayName`, `role`, `order`, `publicationOrganization` — existing importer already handles these. ASCO `body` contains HTML with `\r\n\t<div>` formatting — sanitize_html must handle this.
- **MIRROR**: Existing importer patterns. AACR-2026 notebook cells 16-18 for `AdditionalFields` flattening: `item.update({f"AdditionalFields.{x['Key']}": x["Value"] for x in item["AdditionalFields"]})`. Notebook cells 20-22 for HTML cleaning: `BeautifulSoup(text, "html.parser").get_text()` — our backend uses `bleach.clean()` instead which is already in the importer.
- **IMPORTS**: No new imports.
- **GOTCHA**: AACR-2026 uses `{id}.json` not `{id}_summary.json` — glob pattern `**/*.json` catches both. AACR presentation `AdditionalFields` flattening needed for Topics, Keywords, ePosterClassification. Notebook drops `PlayerUrl` and `PlayerUrlReason` columns — we should skip these in importer. Notebook also drops `Actions` and `AdditionalFields` raw lists after flattening — same approach. ASCO `sessionId` is integer — convert to string. ASCO `primaryTrack` is a dict `{track, trackId}` — extract `.track` for session `track` field.
- **VALIDATE**: Run import for each data source, check counts match file counts. Verify ASCO sessions are created with `sessionTitle` and `sessionType` from presentation data.

### Task 10: Bulk Import Script + Conference Creation
- **ACTION**: Create admin script to create conferences and bulk-import data from all 3 sources in correct order (sessions first for AACR, then presentations).
- **IMPLEMENT**: Create `backend/scripts/import_conferences.py` that: (1) Creates Conference records for AACR-2025, AACR-2026, ASCO-2026. (2) Imports AACR sessions first (from `session/` folder JSON files, with full metadata including AdditionalFields flattening). (3) Imports presentations for all 3 conferences — AACR presentations reference existing sessions; ASCO presentations auto-create sessions from embedded sessionId/sessionTitle/sessionType fields. (4) Runs via `python -m scripts.import_conferences` or API call.
- **MIRROR**: Existing importer API pattern from `app/api/importer.py`. AACR-2026 notebook workflow: sessions first (cell 22), then presentations (cells 16-18), then merge (cell 27). Our import must follow same order.
- **IMPORTS**: `asyncio`, `httpx` (for API calls) or direct SQLAlchemy.
- **GOTCHA**: Import order matters: (a) Create conferences. (b) Import AACR sessions. (c) Import AACR presentations (they reference sessions by SessionId). (d) Import ASCO presentations (auto-creates sessions from embedded data). Conference data: AACR-2025 (Apr 27-30, 2025, Chicago), AACR-2026 (Apr 17-22, 2026, San Diego), ASCO-2026 (May 29-Jun 3, 2026, Chicago). Docker volume mount needed for attachmentFiles access. AACR-2026 notebook uses `pd.merge(df, dat, on="SessionId")` to join session+presentation data — our importer achieves this via SQLAlchemy relationships.
- **VALIDATE**: After running, API returns 3 conferences with correct session/presentation counts. AACR sessions have full metadata (room, description, type). ASCO sessions have titles and types derived from presentation data.

### Task 11: Backend Auth — LDAP Module
- **ACTION**: Create `backend/app/auth/` module with LDAP authentication, session management, and FastAPI dependencies.
- **IMPLEMENT**: `ldap.py`: LDAP bind using `ldap3` library with DN template. `models.py`: Internal User model (id, ldap_uid, display_name, email, role, is_admin). `dependencies.py`: `get_current_user` (optional, returns User or None), `get_admin_user` (required, raises 403 if not admin). `routes.py`: POST `/auth/login` (LDAP bind + session cookie), POST `/auth/logout`, GET `/auth/session` (return current user info). Session via signed cookie (using `itsdangerous` or similar).
- **MIRROR**: FastAPI Depends pattern from existing codebase (e.g., `Depends(get_db)`).
- **IMPORTS**: `ldap3`, `itsdangerous`, `fastapi`, `pydantic`.
- **GOTCHA**: LDAP server config needed in `.env` — LDAP_SERVER, LDAP_BIND_DN_TEMPLATE, LDAP_SEARCH_BASE, LDAP_USER_FILTER. Admin users defined as comma-separated list in config. Anonymous users get no session cookie — `get_current_user` returns None.
- **VALIDATE**: Login with valid LDAP credentials returns session cookie. Invalid credentials return 401. Anonymous request returns no user. Admin user can access admin endpoints.

### Task 12: Backend Auth — Protect Edit/Star Operations
- **ACTION**: Update `interactions.py` and `watchlist.py` to require authentication for write operations, allow anonymous for read operations.
- **IMPLEMENT**: Add `Depends(get_current_user)` to POST/PATCH/DELETE endpoints. Return 401 if user is None. GET endpoints remain public. Watchlist add/remove require auth. Comments/annotations create/update/delete require auth.
- **MIRROR**: Existing endpoint patterns — just add Depends.
- **IMPORTS**: `get_current_user` from `app.auth.dependencies`.
- **GOTCHA**: Watchlist currently uses nullable `user_id` — with auth, user_id should come from authenticated user, not from query param. Anonymous GET watchlist returns empty list (no user context).
- **VALIDATE**: Anonymous user can browse presentations/sessions. Anonymous cannot star/edit. Authenticated user can star/edit.

### Task 13: Frontend Auth — Context + Login UI
- **ACTION**: Create `AuthProvider.tsx`, `useAuth.ts` hook, and integrate with API client and UI.
- **IMPLEMENT**: AuthProvider wraps app, stores user state from `/auth/session` call on mount. useAuth returns `{ user, isAuthenticated, isAdmin, login, logout }`. Login form in Header dropdown. Login calls POST `/auth/login` with username/password. Star button shows login prompt if anonymous.
- **MIRROR**: React context pattern (similar to QueryClientProvider wrapping).
- **IMPORTS**: `react`, `api` (add auth endpoints to client.ts).
- **GOTCHA**: Session cookie is set by backend — frontend just needs to call `/auth/session` on app load. Material Symbols `person` icon for user avatar. If LDAP unavailable, show "Login unavailable" message (graceful degradation).
- **VALIDATE**: Header shows user name when logged in. Star button prompts login when anonymous. Login form validates and calls API.

### Task 14: Docker + Config Updates
- **ACTION**: Update docker-compose.yml, .env, .env.example, pyproject.toml for new dependencies and LDAP config.
- **IMPLEMENT**: Add `ldap3>=2.9.1` to backend dependencies. Add LDAP env vars to .env. Mount `attachmentFiles` volume for importer. Add `itsdangerous>=2.1.0` for session signing.
- **MIRROR**: Existing config pattern from `.env.example`.
- **IMPORTS**: None (config files only).
- **GOTCHA**: LDAP env vars: LDAP_SERVER, LDAP_BIND_DN_TEMPLATE, LDAP_SEARCH_BASE, LDAP_USER_FILTER, ADMIN_USERS. attachmentFiles mount: `- ./attachmentFiles:/data/attachmentFiles:ro`.
- **VALIDATE**: docker-compose builds without errors. Backend starts with new dependencies.

---

## Testing Strategy

### Unit Tests

| Test | Input | Expected Output | Edge Case? |
|---|---|---|---|
| AACR importer - session JSON | `154_summary.json` data | Session with room, start_time, description | Yes — AdditionalFields parsing |
| ASCO importer - nested JSON | `261582.json` nested format | Presentation with authors, tracks, abstract | Yes — nested getContentById |
| LDAP auth - valid credentials | valid username + password | User object with display_name | No |
| LDAP auth - invalid credentials | wrong password | 401 error | Yes |
| LDAP auth - server unavailable | LDAP server down | Graceful error message | Yes |
| Auth dependency - anonymous | No session cookie | `get_current_user` returns None | Yes |
| Auth dependency - admin | Admin user session | `get_admin_user` returns User | No |
| Watchlist - anonymous browse | No auth, GET /watchlist | Empty list | Yes |
| Watchlist - auth star | Authenticated, POST /watchlist | WatchlistItem created | No |

### Edge Cases Checklist
- [ ] Empty presentation data (no abstract)
- [ ] Session with no linked presentations
- [ ] LDAP server unreachable (show fallback)
- [ ] Conference with no sessions (ASCO-2026 only has presentations in files)
- [ ] Duplicate import (same data imported twice — should skip)
- [ ] HTML content in abstract (sanitize correctly)
- [ ] Unicode characters in author names (AACR has non-ASCII)
- [ ] Missing env vars (LDAP_SERVER not set — graceful error)

---

## Validation Commands

### Static Analysis
```bash
cd backend && python -m ruff check app/
cd frontend && npx tsc --noEmit
```
EXPECT: Zero errors

### Unit Tests
```bash
cd backend && python -m pytest tests/ -v
```
EXPECT: All tests pass

### Database Validation
```bash
cd backend && alembic upgrade head
```
EXPECT: Schema up to date with user table

### Browser Validation
```bash
cd frontend && npm run dev
# Open http://localhost:5174
```
EXPECT: Header renders with Material Symbols, Dashboard shows conference cards, calendar grid renders, Sessions page accordion works, Presentations table has all columns, Star page shows login prompt for anonymous

### Data Validation
```bash
# After import script runs:
curl http://localhost:8050/api/conferences | jq '.items | length'
# EXPECT: 3
curl http://localhost:8050/api/sessions?conference_id=<aacr-2025-id> | jq '.total'
# EXPECT: 652 (AACR-2025 session count)
curl http://localhost:8050/api/presentations?conference_id=<asco-2026-id> | jq '.total'
# EXPECT: 7293 (ASCO-2026 presentation count)
```

### Auth Validation
```bash
curl -X POST http://localhost:8050/api/auth/login -d '{"username":"test","password":"test"}'
# EXPECT: 401 or 200 with session cookie
curl http://localhost:8050/api/auth/session
# EXPECT: {"user": null} for anonymous or {"user": {...}} for authenticated
```

### Manual Validation
- [ ] Dashboard renders conference cards with real data
- [ ] Calendar grid shows sessions at correct time slots
- [ ] Sessions page accordion expand/collapse works
- [ ] Presentations table renders with all columns
- [ ] Presentation detail shows abstract, authors, metadata
- [ ] Star button prompts login when anonymous
- [ ] LDAP login flow works end-to-end
- [ ] Authenticated user can star presentations
- [ ] Admin user sees admin controls
- [ ] Footer renders on all pages

---

## Acceptance Criteria
- [ ] All 14 tasks completed
- [ ] Frontend 100% matches demo HTML visual design
- [ ] Real AACR-2025, AACR-2026, ASCO-2026 data imported
- [ ] LDAP authentication works (login/logout/session)
- [ ] Anonymous browsing works for all read operations
- [ ] Authenticated users can star/edit/comment
- [ ] Admin users can access admin functions
- [ ] All validation commands pass
- [ ] No type errors
- [ ] No lint errors

## Completion Checklist
- [ ] Code follows discovered patterns
- [ ] Error handling matches codebase style
- [ ] Logging follows codebase conventions
- [ ] Tests follow test patterns
- [ ] No hardcoded values
- [ ] Documentation updated (if needed)
- [ ] No unnecessary scope additions
- [ ] Self-contained — no questions needed during implementation

## Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LDAP server unavailable in dev | High | Medium | Provide mock LDAP mode for development; env var `LDAP_ENABLED=false` falls back to local auth |
| Demo HTML has hardcoded data | Medium | Low | Map demo data structure to API response types; use real API data |
| AACR session JSON differs from presentation JSON | Medium | Medium | Session JSON has `AdditionalFields` (list of KV pairs), `Date`/`StartTime`/`EndTime`/`Number`/`Location`/`Duration` — separate import method needed. Reference AACR-2026 notebook cells 22-27 for flattening pattern |
| ASCO-2026 has no separate session files — sessions embedded in presentations | Medium | Medium | Extract `sessionId`/`sessionTitle`/`sessionType` from each presentation JSON during import; ASCO sessions are derived, not imported from dedicated files |
| ASCO-2026 JSON is deeply nested GraphQL response | Medium | Low | ASCO importer already handles `getContentById.result` nesting |
| Tailwind v4 token system differs from demo's Tailwind config | Medium | Medium | Use `@theme` block for custom tokens; test all color references |

## Notes
- Demo has a route typo: `/presetation/` instead of `/presentation/` — we fix this in our implementation.
- Demo data is static/hardcoded; our implementation must use real API data while matching the exact visual structure.
- AACR-2025 has 652 session JSON files and 9107 presentation JSON files.
- AACR-2026 has 635 session JSON files and 9644 presentation JSON files.
- ASCO-2026 has 7293 presentation JSON files (no separate session directory — session info is embedded in each presentation JSON as `sessionId`, `sessionTitle`, `sessionType` fields).
- ASCO-2026 JSON format is different (nested `data.getContentById.result`) — importer already handles this. Each presentation contains `sessionId` (integer like 17086), `sessionTitle` ("Care Delivery/Models of Care"), `sessionType` ("Poster Session") — sessions must be extracted from presentation data.
- ASCO-2026 `details/` directory contains 731 paginated search result files (`page-*.json`) with `data.search.result.hits` — these are NOT session detail files, they are search index pages.
- AACR-2026.ipynb notebook shows the complete processing pipeline: (1) download schedule → get presentation IDs, (2) download each presentation detail, (3) flatten `AdditionalFields` as `{f"AdditionalFields.{x['Key']}": x["Value"] for x in item["AdditionalFields"]}`, (4) download session details, (5) flatten session AdditionalFields, (6) merge session + presentation by SessionId, (7) clean HTML with BeautifulSoup, (8) export to Excel. Our importer should follow this same order and flattening approach.
- AACR session JSON `AdditionalFields` contains `SessionName` (for session_type), `AACRTrackAll` (comma-separated tracks), `Presentation Count` (presentation count) — must flatten these into Session model fields.
- WatchlistItem.user_id is currently nullable — with auth, it will be populated from session.
- The `design.md` file is already in the repo root — it should be referenced by CSS tokens, not duplicated in code.
- Frontend currently uses Tailwind v4 with `@import "tailwindcss"` — custom tokens go in `@theme` block in CSS.