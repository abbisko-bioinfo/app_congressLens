import json
from pathlib import Path

from sqlalchemy import select

from app.importers.asco import (
    normalize_name,
    sanitize_html,
    strip_html,
)
from app.importers.base import BaseImporter
from app.models.conference import Conference
from app.models.presentation import Presentation
from app.models.presentation_author import PresentationAuthor
from app.models.presentation_topic import presentation_topics
from app.models.session import Session
from app.models.topic import Topic


class AACRImporter(BaseImporter):
    async def import_folder(self, conference_id: str, folder_path: str) -> dict:
        """Import presentation JSON files from the folder."""
        conference_uuid = conference_id
        conference = await self.db.get(Conference, conference_uuid)
        if not conference:
            return {
                "errors": ["Conference not found"],
                "imported_presentations": 0,
                "imported_sessions": 0,
                "imported_authors": 0,
                "skipped": 0,
            }

        path = Path(folder_path)
        if not path.exists():
            return {
                "errors": ["Folder not found"],
                "imported_presentations": 0,
                "imported_sessions": 0,
                "imported_authors": 0,
                "skipped": 0,
            }

        results = {
            "source": "aacr",
            "imported_presentations": 0,
            "imported_sessions": 0,
            "imported_authors": 0,
            "skipped": 0,
            "errors": [],
        }

        skip_dirs = {"session", "schedule", "focus", "output", "E-Poster-2025AACR_abstract_list", "E-Poster-2025AACR_abstract_list.supp", "On-site_poster", "Oral-2025AACR"}

        batch = 0
        for json_file in sorted(path.glob("**/*.json")):
            # Skip non-presentation subdirectories
            if json_file.parent.name in skip_dirs:
                continue
            try:
                data = json.loads(json_file.read_text())
                await self._import_record(conference_uuid, data, results)
                batch += 1
                if batch % 500 == 0:
                    await self.db.commit()
            except Exception as e:
                await self.db.rollback()
                results["errors"].append(f"{json_file.name}: {str(e)}")
                results["skipped"] += 1

        await self.db.commit()
        return results

    async def import_sessions_folder(self, conference_id: str, folder_path: str) -> dict:
        """Import session JSON files from the session/ subdirectory with full metadata."""
        conference_uuid = conference_id
        conference = await self.db.get(Conference, conference_uuid)
        if not conference:
            return {"errors": ["Conference not found"], "imported_sessions": 0, "skipped": 0}

        path = Path(folder_path)
        if not path.exists():
            return {"errors": ["Folder not found"], "imported_sessions": 0, "skipped": 0}

        results = {"source": "aacr_sessions", "imported_sessions": 0, "skipped": 0, "errors": []}

        # Look for session JSON files — they can be in a session/ subdirectory or mixed in
        session_files = []
        session_subdir = path / "session"
        if session_subdir.exists():
            session_files = sorted(session_subdir.glob("**/*.json"))
        else:
            # Fall back: look for _summary files in the root
            session_files = sorted(path.glob("**/*_summary.json"))

        for json_file in session_files:
            try:
                data = json.loads(json_file.read_text())
                await self._import_session_record(conference_uuid, data, results)
            except Exception as e:
                await self.db.rollback()
                results["errors"].append(f"{json_file.name}: {str(e)}")
                results["skipped"] += 1

        await self.db.commit()
        return results

    async def _import_session_record(self, conference_uuid, data: dict, results: dict):
        """Import a single session JSON with full metadata from AdditionalFields."""
        source_id = data.get("Id")
        if not source_id:
            results["skipped"] += 1
            return

        # Flatten AdditionalFields per notebook pattern
        additional_fields = data.get("AdditionalFields") or []
        flat_fields: dict[str, str] = {}
        for field in additional_fields:
            if isinstance(field, dict) and "Key" in field and "Value" in field:
                flat_fields[f"AdditionalFields.{field['Key']}"] = field["Value"]

        # Extract session metadata from flattened fields
        session_name = flat_fields.get("AdditionalFields.SessionName", "")
        track_all = flat_fields.get("AdditionalFields.AACRTrackAll", "")

        # Build datetime from Date + StartTime/EndTime
        date_val = data.get("Date", "")
        start_time_str = data.get("StartTime", "")
        end_time_str = data.get("EndTime", "")

        start_time = None
        end_time = None
        if date_val and start_time_str:
            try:
                start_time = f"{date_val}T{start_time_str}:00"
            except Exception:
                pass
        if date_val and end_time_str:
            try:
                end_time = f"{date_val}T{end_time_str}:00"
            except Exception:
                pass

        # Check if session already exists (by source_session_id)
        existing = await self.db.scalar(
            select(Session).where(
                Session.conference_id == conference_uuid,
                Session.source_session_id == str(source_id),
            )
        )

        if existing:
            # Update existing session with richer metadata
            existing.title = data.get("Title", existing.title)
            existing.session_type = session_name or data.get("Number", existing.session_type)
            existing.track = track_all or existing.track
            existing.room = data.get("Location", existing.room)
            existing.start_time = start_time or existing.start_time
            existing.end_time = end_time or existing.end_time
            existing.description = strip_html(data.get("Description"))
            await self.db.flush()
            return

        # Create new session with full metadata
        session = Session(
            conference_id=conference_uuid,
            source_session_id=str(source_id),
            title=data.get("Title", ""),
            session_type=session_name or data.get("Number", ""),
            track=track_all,
            room=data.get("Location"),
            start_time=start_time,
            end_time=end_time,
            description=strip_html(data.get("Description")),
        )
        self.db.add(session)
        await self.db.flush()
        results["imported_sessions"] += 1

    async def _import_record(self, conference_uuid, data: dict, results: dict):
        # Skip non-presentation records (schedule files, etc.)
        if not data.get("Id"):
            results["skipped"] += 1
            return
        session_id = await self._ensure_session(conference_uuid, data)

        # Flatten AdditionalFields for presentation-level data
        additional_fields = data.get("AdditionalFields") or []
        flat_fields: dict[str, str] = {}
        for field in additional_fields:
            if isinstance(field, dict) and "Key" in field and "Value" in field:
                flat_fields[f"AdditionalFields.{field['Key']}"] = field["Value"]

        pres_data = {
            "conference_id": conference_uuid,
            "session_id": session_id,
            "source_presentation_id": data.get("Id"),
            "title": data.get("Title", ""),
            "abstract_html": sanitize_html(data.get("Abstract")),
            "abstract_text": strip_html(data.get("Abstract")),
            "presentation_number": data.get("PresentationNumber"),
            "poster_board_number": data.get("PosterboardNumber"),
            "presentation_type": data.get("Activity"),
            "activity": data.get("Activity"),
            "status": data.get("Status"),
            "position_in_session": data.get("PositionInSession"),
            "start_time": data.get("Start"),
            "end_time": data.get("End"),
            "presenter_name": data.get("PresenterDisplayName"),
            "author_block_html": sanitize_html(data.get("AuthorBlock")),
            "disclosure_block_html": sanitize_html(data.get("DisclosureBlock")),
        }

        # Extract institution_block from AdditionalFields
        institution = flat_fields.get("AdditionalFields.Institution")
        if institution:
            pres_data["institution_block"] = institution

        pres = Presentation(**pres_data)
        self.db.add(pres)
        await self.db.flush()
        results["imported_presentations"] += 1

        await self._parse_authors(pres.id, data, results)
        await self._import_topics(pres.id, data, flat_fields)

    async def _ensure_session(self, conference_uuid, data: dict):
        source_id = data.get("SessionId")
        if not source_id:
            return None

        existing = await self.db.scalar(
            select(Session).where(
                Session.conference_id == conference_uuid,
                Session.source_session_id == str(source_id),
            )
        )
        if existing:
            return existing.id

        session = Session(
            conference_id=conference_uuid,
            source_session_id=str(source_id),
            title=data.get("SessionTitle", ""),
            session_type=data.get("Activity"),
        )
        self.db.add(session)
        await self.db.flush()
        return session.id

    async def _parse_authors(self, presentation_id, data: dict, results: dict):
        author_block = data.get("AuthorBlock", "")
        if not author_block:
            return
        stripped = strip_html(author_block) or ""
        parts = [p.strip() for p in stripped.split(";") if p.strip()]
        for i, part in enumerate(parts):
            name_and_aff = part.strip()
            name = name_and_aff.split("(")[0].strip() if "(" in name_and_aff else name_and_aff
            org = name_and_aff.split("(")[1].rstrip(")").strip() if "(" in name_and_aff else None
            obj = PresentationAuthor(
                presentation_id=presentation_id,
                display_name=name,
                normalized_name=normalize_name(name),
                author_order=i + 1,
                organization=org,
                is_first_author=(i == 0),
                is_presenter=(name == data.get("PresenterDisplayName")),
            )
            self.db.add(obj)
        await self.db.flush()
        results["imported_authors"] += len(parts)

    async def _import_topics(self, presentation_id, data: dict, flat_fields: dict):
        raw_topics: list[str] = []

        # Extract topics from flattened AdditionalFields
        keywords = flat_fields.get("AdditionalFields.Keywords")
        if keywords:
            if isinstance(keywords, str):
                raw_topics.extend([k.strip() for k in keywords.split(",") if k.strip()])
            elif isinstance(keywords, list):
                raw_topics.extend(keywords)

        topic_cat = flat_fields.get("AdditionalFields.Topic")
        if topic_cat:
            if isinstance(topic_cat, str):
                raw_topics.extend([t.strip() for t in topic_cat.split(",") if t.strip()])
            elif isinstance(topic_cat, list):
                raw_topics.extend(topic_cat)

        eposter = flat_fields.get("AdditionalFields.ePosterClassification")
        if eposter:
            if isinstance(eposter, str):
                raw_topics.extend([t.strip() for t in eposter.split(",") if t.strip()])
            elif isinstance(eposter, list):
                raw_topics.extend(eposter)

        # Also check raw AdditionalFields dict for Topics
        for field in data.get("AdditionalFields") or []:
            if isinstance(field, dict):
                key = field.get("Key", "")
                if key in ("Keywords", "Topic", "Category", "Track"):
                    val = field.get("Value", "")
                    if isinstance(val, str):
                        raw_topics.extend([v.strip() for v in val.split(",") if v.strip()])
                    elif isinstance(val, list):
                        raw_topics.extend(val)

        for topic_name in raw_topics:
            name = topic_name.strip()
            if not name:
                continue
            norm = normalize_name(name)
            existing = await self.db.scalar(
                select(Topic).where(
                    Topic.normalized_name == norm, Topic.type == "keyword"
                )
            )
            if not existing:
                topic = Topic(name=name, normalized_name=norm, type="keyword")
                self.db.add(topic)
                await self.db.flush()
                existing = topic
            await self.db.execute(
                presentation_topics.insert().values(
                    presentation_id=presentation_id, topic_id=existing.id
                )
            )
