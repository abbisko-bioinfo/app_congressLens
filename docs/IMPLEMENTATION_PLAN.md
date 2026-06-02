# CongressLens Implementation Plan

## 1. Implementation Overview

Build CongressLens as a Docker Compose deployed full-stack application:

- React frontend
- FastAPI backend
- PostgreSQL database
- MinIO object storage
- Redis queue
- Worker service

The first implementation milestone should create a working MVP that can import normalized presentation data, browse conferences/sessions/presentations, preview attachments, and support comments, annotations, and watchlist calendar.

Raw JSON files are only references for importer and schema design. They must not be stored as raw JSON records.

## 2. Repository Structure

Create the following structure:

```text
CongressLens/
  backend/
    app/
      api/
      core/
      db/
      importers/
      models/
      schemas/
      services/
      workers/
      main.py
    alembic/
    tests/
    pyproject.toml
    Dockerfile

  frontend/
    src/
      api/
      components/
      pages/
      routes/
      styles/
      types/
    package.json
    vite.config.ts
    Dockerfile

  docs/
    PRD.md
    IMPLEMENTATION_PLAN.md

  docker-compose.yml
  .env.example
  README.md
```

## 3. Phase 1 - Docker Compose Foundation

### 3.1 Add Docker Compose Services

Create `docker-compose.yml` with:

- postgres
- minio
- redis
- backend
- worker
- frontend

Recommended ports:

```text
Frontend:   http://localhost:5173
Backend:    http://localhost:8000
PostgreSQL: localhost:5432
MinIO API:  http://localhost:9000
MinIO UI:   http://localhost:9001
Redis:      localhost:6379
```

### 3.2 Environment Variables

Create `.env.example`:

```text
POSTGRES_DB=congresslens
POSTGRES_USER=congresslens
POSTGRES_PASSWORD=congresslens-password
DATABASE_URL=postgresql+psycopg://congresslens:congresslens-password@postgres:5432/congresslens

MINIO_ENDPOINT=minio:9000
MINIO_PUBLIC_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=congresslens
MINIO_SECRET_KEY=congresslens-password
MINIO_BUCKET=congresslens-attachments
MINIO_SECURE=false

REDIS_URL=redis://redis:6379/0

BACKEND_CORS_ORIGINS=http://localhost:5173
```

### 3.3 Acceptance Criteria

- `docker compose up` starts all infrastructure services.
- PostgreSQL is reachable from backend.
- MinIO UI is reachable.
- Redis is reachable from worker.

## 4. Phase 2 - Backend Foundation

### 4.1 FastAPI Setup

Implement:

- `backend/app/main.py`
- app config loading
- CORS
- health endpoint
- API router registration

Health endpoints:

```text
GET /health
GET /api/health
```

### 4.2 Database Setup

Use SQLAlchemy or SQLModel with Alembic.

Implement:

- database session dependency
- model definitions
- Alembic migrations
- timestamp helpers

Required initial models:

- Conference
- Session
- Presentation
- PresentationAuthor
- Topic
- Attachment
- Comment
- Annotation
- WatchlistItem
- AISummary
- PresentationEntity

### 4.3 Acceptance Criteria

- Backend starts without database errors.
- Alembic migration creates all MVP tables.
- Health endpoint returns success.

## 5. Phase 3 - Unified Database Implementation

### 5.1 Implement Core Tables

Create database models matching the unified schema in `docs/PRD.md`:

- conferences
- sessions
- presentations
- presentation_authors
- topics
- presentation_topics
- session_topics
- attachments
- comments
- annotations
- watchlist_items
- ai_summaries
- presentation_entities

### 5.2 Data Rules

Implement these rules:

- No raw JSON table.
- No raw JSON column.
- UUID primary keys.
- `created_at` and `updated_at` on mutable tables.
- PostgreSQL arrays may be used for `funding_sources`.
- `abstract_html`, `author_block_html`, and `disclosure_block_html` are stored as sanitized HTML.

### 5.3 Search Support

Add search indexes or backend search logic for:

- presentation title
- abstract text
- author display name
- organization
- presentation number
- abstract number
- DOI
- clinical trial registry number

### 5.4 Acceptance Criteria

- Migrations apply cleanly.
- All foreign keys are valid.
- Presentation can be queried with authors and topics.
- No raw JSON is persisted.

## 6. Phase 4 - Backend API

### 6.1 Conference APIs

Implement:

```text
GET    /api/conferences
POST   /api/conferences
GET    /api/conferences/{id}
PATCH  /api/conferences/{id}
```

### 6.2 Session APIs

Implement:

```text
GET    /api/sessions?conference_id=
POST   /api/sessions
GET    /api/sessions/{id}
PATCH  /api/sessions/{id}
```

### 6.3 Presentation APIs

Implement:

```text
GET    /api/presentations
POST   /api/presentations
GET    /api/presentations/{id}
PATCH  /api/presentations/{id}
GET    /api/presentations/{id}/authors
```

List endpoint filters:

- conference_id
- session_id
- query
- author
- organization
- topic
- presentation_type
- watched
- has_attachment
- summary_status

### 6.4 Comments, Annotations, Watchlist

Implement:

```text
GET    /api/presentations/{id}/comments
POST   /api/presentations/{id}/comments
PATCH  /api/comments/{id}
DELETE /api/comments/{id}

GET    /api/presentations/{id}/annotations
POST   /api/presentations/{id}/annotations
PATCH  /api/annotations/{id}
DELETE /api/annotations/{id}

GET    /api/watchlist
POST   /api/watchlist
DELETE /api/watchlist/{id}
GET    /api/calendar/events
```

### 6.5 Acceptance Criteria

- API supports CRUD for MVP entities.
- Presentation detail response includes authors, topics, attachments, comments, annotations, and watch status.
- Calendar events include watched conferences, sessions, and presentations.

## 7. Phase 5 - Presentation Importers

### 7.1 Importer Structure

Create:

```text
backend/app/importers/base.py
backend/app/importers/asco.py
backend/app/importers/aacr.py
```

### 7.2 ASCO Importer

Reference shape:

```text
data.getContentById.result
```

Map fields:

- `presentationId` or `contentId` -> source_presentation_id/source_content_id
- `title` -> title
- `body` -> abstract_html
- HTML-stripped body -> abstract_text
- `sessionTitle` -> session.title
- `sessionType` -> session.session_type
- `sessionId` -> session.source_session_id
- `abstractNumber` -> abstract_number
- `posterBoardNumber` -> poster_board_number
- `clinicalTrialRegistryNumber` -> clinical_trial_registry_number
- `journalCitation` -> journal_citation
- `doi` -> doi
- `fundingSources` -> funding_sources
- `additionalFundingSource` -> additional_funding_source
- `authors` -> presentation_authors
- `firstAuthor` -> first author fields
- `presenter` -> presenter fields
- `tracks`, `primaryTrack`, `subtrack`, `taxonomyFacet` -> topics/tracks
- `publishDate.start/end/timeZone` -> presentation start/end/timezone
- `presentationUrl` -> source_url
- `disclosureUrl` -> disclosure_url
- `hasAbstract`, `hasSlides`, `hasPosters`, `hasVideos` -> availability flags

### 7.3 AACR Importer

Reference shape:

```text
Top-level JSON fields
```

Map fields:

- `Id` -> source_presentation_id
- `Title` -> title
- `Abstract` -> abstract_html and abstract_text
- `SessionId` -> session.source_session_id
- `SessionTitle` -> session.title
- `Activity` -> activity/presentation_type
- `Status` -> status
- `Start` / `End` -> presentation start/end
- `PositionInSession` -> position_in_session
- `PresentationNumber` -> presentation_number
- `PosterboardNumber` -> poster_board_number
- `PresenterDisplayName` -> presenter_name
- `PresenterBiography` -> presenter_biography if model support is added later
- `AuthorBlock` -> author_block_html and parsed author/institution data
- `DisclosureBlock` -> disclosure_block_html
- `AdditionalFields` topics/keywords -> topics
- `PresentationFiles`, `AdditionalFiles`, `PlayerUrl`, `ThumbnailUrl` -> optional attachment/media references if available

### 7.4 HTML Cleanup

Implement sanitation for:

- `abstract_html`
- `author_block_html`
- `disclosure_block_html`

Allowed HTML:

- p
- br
- b
- strong
- i
- em
- u
- sup
- sub
- table
- thead
- tbody
- tr
- th
- td
- div
- span
- img

For images:

- allow `data:image/*;base64` during MVP
- allow safe HTTP/HTTPS URLs
- remove scripts and event handlers

### 7.5 Import API

Implement:

```text
POST /api/import/conferences/{conference_id}/presentations
```

Request:

```json
{
  "source": "asco",
  "folder_path": "attachmentFiles/ASCO-2026/presentation"
}
```

Response:

```json
{
  "source": "asco",
  "imported_presentations": 100,
  "imported_sessions": 10,
  "imported_authors": 450,
  "skipped": 0,
  "errors": []
}
```

### 7.6 Acceptance Criteria

- ASCO sample files import into normalized tables.
- AACR sample files import into normalized tables.
- Author order is preserved when available.
- Presenter and first author are correctly marked when available.
- No raw JSON is stored.

## 8. Phase 6 - MinIO Attachment Service

### 8.1 MinIO Setup

Implement:

- MinIO client service
- bucket creation on startup or initialization command
- upload helper
- delete helper
- presigned preview URL helper
- presigned download URL helper

### 8.2 Attachment APIs

Implement:

```text
GET    /api/presentations/{id}/attachments
POST   /api/presentations/{id}/attachments
GET    /api/attachments/{id}/preview
GET    /api/attachments/{id}/download
DELETE /api/attachments/{id}
```

### 8.3 Preview Rules

Implement:

- PDF: `preview_status=ready`, preview uses original object key.
- Image: `preview_status=ready`, preview uses original object key.
- PPTX: `preview_status=pending`, worker task queued.
- DOCX: `preview_status=pending`, worker task queued.
- XLSX: `preview_status=not_supported` for MVP.
- Unknown: `preview_status=not_supported`.

### 8.4 Acceptance Criteria

- File upload stores object in MinIO.
- Attachment metadata is saved in PostgreSQL.
- PDF/image preview endpoint returns presigned URL.
- Unsupported files return download fallback.

## 9. Phase 7 - Worker Service

### 9.1 Worker Foundation

Use Redis-backed worker tooling such as RQ, Celery, or Dramatiq.

Implement task names:

- `convert_attachment_preview`
- `generate_presentation_summary`
- `extract_presentation_entities`
- `generate_conference_summary`

MVP only needs `convert_attachment_preview` placeholder behavior.

### 9.2 Attachment Conversion Placeholder

For PPTX/DOCX:

- set `preview_status=processing`
- attempt conversion only if conversion tooling is installed
- otherwise set `preview_status=not_supported` or `failed` with `conversion_error`

### 9.3 Acceptance Criteria

- Worker starts in Docker Compose.
- Attachment upload can enqueue a worker job.
- Failed or unsupported conversion does not block file upload.

## 10. Phase 8 - Frontend Foundation

### 10.1 React Setup

Use:

- Vite
- TypeScript
- React Router
- TanStack Query
- CSS modules or Tailwind CSS

Recommended UI style:

- dense operational interface
- left navigation
- compact tables
- restrained colors
- no landing page

### 10.2 App Routes

Implement:

```text
/
/conferences
/conferences/:conferenceId
/sessions/:sessionId
/presentations
/presentations/:presentationId
/calendar
```

### 10.3 API Client

Create typed API client methods for:

- conferences
- sessions
- presentations
- attachments
- comments
- annotations
- watchlist
- calendar

### 10.4 Acceptance Criteria

- Frontend starts with Docker Compose.
- API base URL is configurable.
- Main routes render without errors.

## 11. Phase 9 - Frontend Pages

### 11.1 Dashboard

Implement:

- watched presentations
- upcoming watched sessions
- recent presentations
- AI placeholder panel

### 11.2 Conference Pages

Implement:

- conference list
- conference detail
- sessions tab
- presentations tab
- calendar tab
- insights placeholder tab

### 11.3 Session Pages

Implement:

- session metadata
- presentation list filtered by session

### 11.4 Presentation List

Implement table columns:

- title
- conference
- session
- presentation number
- abstract number
- presenter
- first author
- organization
- presentation type
- start time
- watched
- has slides/poster/video

Implement filters:

- conference
- session
- query
- author
- organization
- topic
- presentation type
- watched
- has attachment
- summary status

### 11.5 Presentation Detail

Implement sections:

- header metadata
- author/institution panel
- abstract viewer
- attachment viewer
- funding/disclosure panel
- comments
- annotations
- AI summary placeholder

### 11.6 Calendar

Use FullCalendar or React Big Calendar.

Implement:

- watched conference events
- watched session events
- watched presentation events
- click-through navigation
- conference color coding

### 11.7 Acceptance Criteria

- Presentation details display all required metadata.
- Author list is sorted by author order.
- Abstract HTML supports tables and images.
- Watched items appear in calendar.

## 12. Phase 10 - Attachment Viewer UI

### 12.1 Viewer Components

Create:

- AttachmentList
- AttachmentViewer
- PdfViewer
- ImageViewer
- UnsupportedAttachmentFallback
- UploadAttachmentButton

### 12.2 Behavior

- PDF opens inside presentation detail page.
- Image opens inside presentation detail page.
- Unsupported types show metadata and download action.
- PPTX/DOCX show conversion status.

### 12.3 Acceptance Criteria

- PDF/image preview works without downloading.
- Unsupported file has clear fallback.
- Upload progress and upload errors are visible.

## 13. Phase 11 - AI Summary Preparation

### 13.1 Backend

Implement:

- `ai_summaries` model and API read endpoint
- `presentation_entities` model
- worker task placeholders

Optional MVP API:

```text
GET  /api/presentations/{id}/ai-summary
POST /api/presentations/{id}/ai-summary/jobs
```

### 13.2 Frontend

Implement:

- AI Summary panel on presentation detail
- Insights tab on conference detail
- Empty state when no summary exists

### 13.3 Acceptance Criteria

- AI panels render without real AI integration.
- Summary status can be displayed.
- Future worker tasks have a clear integration point.

## 14. Phase 12 - Testing

### 14.1 Backend Tests

Add tests for:

- health endpoint
- database migrations
- conference CRUD
- session CRUD
- presentation CRUD
- presentation author relationship
- ASCO importer
- AACR importer
- attachment upload metadata
- MinIO presigned URL generation
- comments CRUD
- annotations CRUD
- watchlist/calendar behavior

### 14.2 Frontend Tests

Add tests for:

- main route rendering
- conference list rendering
- presentation list filters
- presentation detail metadata display
- author list ordering
- attachment viewer fallback states
- calendar event rendering

### 14.3 Integration Tests

Manual or automated scenarios:

- Docker Compose starts full stack.
- Import ASCO sample folder.
- Import AACR sample folder.
- Open conference detail.
- Open presentation detail.
- Upload PDF.
- Preview PDF in page.
- Add comment.
- Add annotation.
- Watch presentation.
- Confirm presentation appears in calendar.

## 15. Phase 13 - Documentation And Developer Workflow

### 15.1 README

Document:

- project overview
- Docker Compose startup
- environment setup
- migration commands
- import commands
- development URLs

### 15.2 Developer Commands

Recommended commands:

```text
docker compose up
docker compose exec backend alembic upgrade head
docker compose exec backend pytest
docker compose exec frontend npm test
```

### 15.3 Acceptance Criteria

- A new developer can start the stack using README instructions.
- Import workflow is documented.
- API docs are available from FastAPI Swagger.

## 16. Implementation Order

Recommended coding order:

1. Docker Compose infrastructure.
2. Backend app foundation.
3. Database models and migrations.
4. Conference/session/presentation APIs.
5. Importers for ASCO and AACR.
6. Frontend app shell.
7. Conference/session/presentation pages.
8. MinIO attachment upload.
9. Attachment preview UI.
10. Comments, annotations, watchlist.
11. Calendar.
12. Worker placeholder.
13. AI summary placeholders.
14. Tests.
15. README and operational docs.

## 17. Final MVP Acceptance Checklist

- Full stack starts with Docker Compose.
- PostgreSQL schema is unified and contains no raw JSON storage.
- ASCO and AACR JSON references can be imported into normalized records.
- Presentation page displays complete content, authors, and institutions.
- Attachments are stored in MinIO.
- PDF/image attachments preview inside presentation page.
- Comments and annotations work.
- Watchlist and calendar work.
- AI summary placeholders are visible and ready for future implementation.

