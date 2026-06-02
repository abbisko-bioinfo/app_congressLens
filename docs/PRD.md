# CongressLens PRD

## 1. Product Summary

CongressLens is a web application for managing and analyzing oncology conference presentations from AACR, ASCO, ESMO, and similar conferences.

The application will provide structured conference/session/presentation browsing, full presentation metadata display, author and institution tracking, attachment preview, user comments, annotations, watchlist calendar, and future AI-powered conference intelligence features.

The initial system will use:

- Frontend: React, TypeScript, Vite
- Backend: FastAPI
- Database: PostgreSQL
- Object storage: MinIO
- Deployment: Docker Compose
- Worker: background jobs for attachment preview conversion and future AI tasks
- Redis: background task queue dependency

The existing JSON files under `attachmentFiles/ASCO-2026/presentation/` and `attachmentFiles/AACR-2026/presentation-updated/` are only schema references for database and importer design. The app will not preserve raw JSON data in PostgreSQL.

## 2. Target Users

Primary users:

- Oncology competitive intelligence analysts
- Pharmaceutical R&D and strategy teams
- Business development teams
- Medical affairs teams
- Healthcare investors and research analysts

Primary user needs:

- Track important conference presentations across AACR, ASCO, ESMO, and related oncology meetings.
- Review presentation content with full author, institution, abstract, disclosure, funding, DOI, and clinical trial metadata.
- Attach internal files and preview them directly inside the presentation page.
- Comment, annotate, and mark important presentations for follow-up.
- Use a calendar to follow conference sessions and watched presentations.
- Later use AI summary and trend dashboards to identify active companies, hot targets, new drugs, clinical updates, and emerging research themes.

## 3. Product Goals

### 3.1 MVP Goals

- Provide a structured conference browser.
- Provide session and presentation browsing.
- Display complete presentation details, including authors and institutions.
- Support PDF/image attachment upload and in-page preview.
- Store all files in MinIO.
- Store all business data in PostgreSQL.
- Support comments, annotations, and watchlist.
- Show watched conferences, sessions, and presentations in a calendar.
- Deploy the complete local stack with Docker Compose.

### 3.2 Future Goals

- Generate AI summaries for presentations, sessions, and conferences.
- Extract companies, drugs, targets, indications, biomarkers, modalities, and clinical phases.
- Build target/company trend dashboards.
- Compare activity across conferences, such as AACR vs ASCO vs ESMO.
- Generate conference insight reports and weekly update reports.

## 4. MVP Scope

### 4.1 Conference Management

Users can:

- View all conferences.
- Open a conference detail page.
- See conference date, year, location, acronym, and presentation/session counts.
- Navigate to sessions, presentations, calendar, and insights placeholder pages.

### 4.2 Session Management

Users can:

- View sessions under a conference.
- Filter sessions by type, track, time, and keyword.
- Open a session detail page.
- See all presentations under the session.

### 4.3 Presentation Management

Users can:

- View presentation lists.
- Search presentations by title, abstract, author, institution, presentation number, abstract number, DOI, trial number, topic, and keyword.
- Filter presentations by conference, session, track, presentation type, watched status, attachment status, and AI summary status.
- Open a presentation detail page.

Presentation detail must display:

- Title
- Conference
- Session
- Session type
- Track and subtrack
- Presentation type/activity
- Status
- Start/end time
- Presentation number
- Abstract number
- Poster board number
- Presenter
- First author
- Full author list
- Author institutions
- Author block HTML, when available
- Abstract HTML
- Disclosure block
- Funding sources
- DOI
- Journal citation
- Clinical trial registry number
- Source URL
- Slides/poster/video availability flags
- Attachments
- Comments
- Annotations
- Watch status
- AI summary placeholder

### 4.4 Author And Institution Tracking

Authors must be stored separately from presentations.

The system must support:

- Ordered author lists
- Presenter identification
- First author identification
- Author role
- Organization/institution display
- Source-specific author IDs where available
- Normalized names for future search and analytics

### 4.5 Attachment Management

Users can:

- Upload files to a presentation.
- See attachment metadata.
- Preview supported attachments directly inside the presentation page.
- Download files if preview is unavailable.
- Delete attachments.

Supported MVP preview behavior:

- PDF: in-page viewer.
- Image: in-page viewer.
- PPTX: upload supported; preview conversion status shown.
- DOCX: upload supported; preview conversion status shown.
- XLSX: upload supported; download fallback in MVP.
- Unsupported files: download fallback.

### 4.6 Comments

Users can:

- Add presentation comments.
- Edit comments.
- Delete comments.
- View comment timeline.

MVP may use a single default user without authentication.

### 4.7 Annotations

Users can:

- Add text annotations to a presentation.
- Add attachment/page-level annotations when possible.
- Use colors for annotation categorization.
- Edit and delete annotations.

### 4.8 Watchlist And Calendar

Users can:

- Watch conferences, sessions, and presentations.
- View watched items in a calendar.
- Click calendar items to open related detail pages.

Calendar items should include:

- Conference date ranges
- Watched session time blocks
- Watched presentation time blocks

### 4.9 AI Placeholder

MVP will not implement real AI generation yet, but must reserve:

- AI summary database structure
- Presentation detail AI summary panel
- Conference insights tab
- Worker task naming and status conventions

## 5. Non-MVP Scope

The following are excluded from the first coding milestone but should be supported by architecture:

- Multi-user authentication and authorization
- Real AI model integration
- Full PPTX/DOCX-to-PDF conversion implementation
- Entity extraction production workflow
- Trend scoring algorithm
- Report export
- External calendar sync
- Conference website crawler
- SSO

## 6. Unified Database Structure

PostgreSQL is the single source of truth for business data. MinIO is the single source of truth for file objects.

Raw JSON source files will not be stored in PostgreSQL. Importers will read JSON files, normalize fields, write structured records, and discard raw JSON after import.

### 6.1 conferences

Purpose: stores conference-level data.

Columns:

- id: UUID primary key
- acronym: text, required
- name: text, required
- year: integer, required
- location: text, nullable
- start_date: date, nullable
- end_date: date, nullable
- timezone: text, nullable
- website: text, nullable
- description: text, nullable
- created_at: timestamptz, required
- updated_at: timestamptz, required

Unique constraint:

- acronym + year

### 6.2 sessions

Purpose: stores conference session data.

Columns:

- id: UUID primary key
- conference_id: UUID foreign key to conferences.id
- source_session_id: text, nullable
- title: text, required
- session_type: text, nullable
- track: text, nullable
- subtrack: text, nullable
- room: text, nullable
- start_time: timestamptz, nullable
- end_time: timestamptz, nullable
- timezone: text, nullable
- description: text, nullable
- is_on_demand: boolean, default false
- created_at: timestamptz, required
- updated_at: timestamptz, required

Indexes:

- conference_id
- source_session_id
- start_time
- title full-text/search index

### 6.3 presentations

Purpose: stores normalized presentation data.

Columns:

- id: UUID primary key
- conference_id: UUID foreign key to conferences.id
- session_id: UUID nullable foreign key to sessions.id
- source_presentation_id: text, nullable
- source_content_id: text, nullable
- title: text, required
- abstract_text: text, nullable
- abstract_html: text, nullable
- presentation_number: text, nullable
- abstract_number: text, nullable
- poster_board_number: text, nullable
- presentation_type: text, nullable
- activity: text, nullable
- status: text, nullable
- position_in_session: integer, nullable
- start_time: timestamptz, nullable
- end_time: timestamptz, nullable
- timezone: text, nullable
- presenter_name: text, nullable
- first_author_name: text, nullable
- author_block_html: text, nullable
- institution_block: text, nullable
- disclosure_block_html: text, nullable
- funding_sources: text array, nullable
- additional_funding_source: text, nullable
- doi: text, nullable
- journal_citation: text, nullable
- clinical_trial_registry_number: text, nullable
- source_url: text, nullable
- disclosure_url: text, nullable
- has_abstract: boolean, default false
- has_slides: boolean, default false
- has_posters: boolean, default false
- has_videos: boolean, default false
- summary_status: text, default `none`
- created_at: timestamptz, required
- updated_at: timestamptz, required

Allowed summary_status values:

- none
- pending
- processing
- ready
- failed

Indexes:

- conference_id
- session_id
- source_presentation_id
- source_content_id
- presentation_number
- abstract_number
- doi
- clinical_trial_registry_number
- start_time
- summary_status
- title full-text/search index
- abstract_text full-text/search index

### 6.4 presentation_authors

Purpose: stores authors separately for display, search, and future analytics.

Columns:

- id: UUID primary key
- presentation_id: UUID foreign key to presentations.id
- source_author_id: text, nullable
- display_name: text, required
- normalized_name: text, nullable
- role: text, nullable
- author_order: integer, nullable
- organization: text, nullable
- city: text, nullable
- country: text, nullable
- picture_url: text, nullable
- is_first_author: boolean, default false
- is_presenter: boolean, default false
- created_at: timestamptz, required
- updated_at: timestamptz, required

Indexes:

- presentation_id
- normalized_name
- organization
- author_order
- is_first_author
- is_presenter

### 6.5 topics

Purpose: stores normalized topics, keywords, tracks, and subtracks.

Columns:

- id: UUID primary key
- name: text, required
- normalized_name: text, required
- type: text, required
- created_at: timestamptz, required
- updated_at: timestamptz, required

Allowed type values:

- topic
- keyword
- track
- subtrack

Unique constraint:

- normalized_name + type

### 6.6 presentation_topics

Purpose: many-to-many relationship between presentations and topics.

Columns:

- presentation_id: UUID foreign key to presentations.id
- topic_id: UUID foreign key to topics.id

Primary key:

- presentation_id + topic_id

### 6.7 session_topics

Purpose: many-to-many relationship between sessions and topics.

Columns:

- session_id: UUID foreign key to sessions.id
- topic_id: UUID foreign key to topics.id

Primary key:

- session_id + topic_id

### 6.8 attachments

Purpose: stores MinIO-backed attachment metadata.

Columns:

- id: UUID primary key
- presentation_id: UUID foreign key to presentations.id
- original_filename: text, required
- original_object_key: text, required
- bucket_name: text, required
- content_type: text, nullable
- file_size: bigint, nullable
- preview_object_key: text, nullable
- preview_content_type: text, nullable
- preview_status: text, default `pending`
- conversion_error: text, nullable
- uploaded_by: text, nullable
- uploaded_at: timestamptz, required

Allowed preview_status values:

- pending
- processing
- ready
- failed
- not_supported

Indexes:

- presentation_id
- preview_status
- content_type

### 6.9 comments

Purpose: stores presentation comments.

Columns:

- id: UUID primary key
- presentation_id: UUID foreign key to presentations.id
- author: text, nullable
- body: text, required
- created_at: timestamptz, required
- updated_at: timestamptz, required

Indexes:

- presentation_id
- created_at

### 6.10 annotations

Purpose: stores presentation and attachment annotations.

Columns:

- id: UUID primary key
- presentation_id: UUID foreign key to presentations.id
- attachment_id: UUID nullable foreign key to attachments.id
- selected_text: text, nullable
- note: text, required
- color: text, nullable
- page_number: integer, nullable
- anchor_data: jsonb, nullable
- created_by: text, nullable
- created_at: timestamptz, required
- updated_at: timestamptz, required

Indexes:

- presentation_id
- attachment_id
- created_at

### 6.11 watchlist_items

Purpose: stores watched conferences, sessions, and presentations.

Columns:

- id: UUID primary key
- user_id: text, nullable
- target_type: text, required
- target_id: UUID, required
- note: text, nullable
- created_at: timestamptz, required

Allowed target_type values:

- conference
- session
- presentation

Unique constraint:

- user_id + target_type + target_id

For MVP, user_id can be null or a fixed default user value.

### 6.12 ai_summaries

Purpose: stores future AI-generated summaries.

Columns:

- id: UUID primary key
- scope_type: text, required
- scope_id: UUID, required
- summary_type: text, required
- content: text, nullable
- model_name: text, nullable
- status: text, default `pending`
- created_at: timestamptz, required
- updated_at: timestamptz, required

Allowed scope_type values:

- presentation
- session
- conference

Allowed status values:

- pending
- processing
- ready
- failed

### 6.13 presentation_entities

Purpose: stores future AI/entity extraction outputs.

Columns:

- id: UUID primary key
- presentation_id: UUID foreign key to presentations.id
- entity_type: text, required
- entity_name: text, required
- normalized_name: text, nullable
- confidence: numeric, nullable
- evidence_text: text, nullable
- created_at: timestamptz, required

Allowed entity_type examples:

- company
- drug
- target
- indication
- biomarker
- modality
- clinical_phase

## 7. MinIO Object Storage Design

Bucket:

```text
congresslens-attachments
```

Original file object key:

```text
conferences/{conference_id}/presentations/{presentation_id}/{attachment_id}/original/{filename}
```

Preview file object key:

```text
conferences/{conference_id}/presentations/{presentation_id}/{attachment_id}/preview/{filename}.pdf
```

Rules:

- Frontend never receives MinIO credentials.
- Backend uploads files to MinIO.
- Backend generates short-lived presigned URLs for preview and download.
- PostgreSQL stores only metadata and object keys.

## 8. Main Pages

### 8.1 Dashboard

Includes:

- Watched presentations
- Upcoming watched sessions
- Recently updated presentations
- AI insights placeholder

### 8.2 Conferences

Includes:

- Conference list
- Conference detail
- Overview tab
- Sessions tab
- Presentations tab
- Calendar tab
- Insights placeholder tab

### 8.3 Sessions

Includes:

- Session metadata
- Presentation list
- Track/topic display

### 8.4 Presentations

Includes:

- Searchable/filterable presentation table
- Presentation detail workspace
- Full author and institution display
- Abstract HTML viewer
- Attachment viewer
- Comments
- Annotations
- Watch button
- AI summary placeholder

### 8.5 Calendar

Includes:

- Conference date ranges
- Watched sessions
- Watched presentations
- Color coding by conference acronym

## 9. Public API Requirements

The backend will expose REST APIs under `/api`.

### Conferences

```text
GET    /api/conferences
POST   /api/conferences
GET    /api/conferences/{id}
PATCH  /api/conferences/{id}
```

### Sessions

```text
GET    /api/sessions?conference_id=
POST   /api/sessions
GET    /api/sessions/{id}
PATCH  /api/sessions/{id}
```

### Presentations

```text
GET    /api/presentations
POST   /api/presentations
GET    /api/presentations/{id}
PATCH  /api/presentations/{id}
GET    /api/presentations/{id}/authors
```

### Attachments

```text
GET    /api/presentations/{id}/attachments
POST   /api/presentations/{id}/attachments
GET    /api/attachments/{id}/preview
GET    /api/attachments/{id}/download
DELETE /api/attachments/{id}
```

### Comments

```text
GET    /api/presentations/{id}/comments
POST   /api/presentations/{id}/comments
PATCH  /api/comments/{id}
DELETE /api/comments/{id}
```

### Annotations

```text
GET    /api/presentations/{id}/annotations
POST   /api/presentations/{id}/annotations
PATCH  /api/annotations/{id}
DELETE /api/annotations/{id}
```

### Watchlist And Calendar

```text
GET    /api/watchlist
POST   /api/watchlist
DELETE /api/watchlist/{id}
GET    /api/calendar/events
```

### Import

```text
POST /api/import/conferences/{conference_id}/presentations
```

Import behavior:

- Input: source type and JSON folder path or uploaded JSON files.
- Output: imported counts and skipped/error counts.
- Raw JSON is not stored.
- Parsed and normalized data is stored in PostgreSQL.

## 10. Acceptance Criteria

MVP is accepted when:

- `docker compose up` starts frontend, backend, PostgreSQL, MinIO, Redis, and worker.
- Backend migrations create the unified schema.
- ASCO and AACR reference JSON formats can be imported into normalized tables.
- Presentation detail page shows title, metadata, authors, institutions, abstract, disclosure, funding, DOI, trial number, and session context.
- PDF and image attachments can be uploaded and previewed inside the presentation page.
- PPTX and DOCX uploads show conversion status even if conversion is not yet implemented.
- Comments, annotations, and watchlist work.
- Calendar displays watched conferences, sessions, and presentations.
- No raw JSON table or raw JSON persistence exists.

