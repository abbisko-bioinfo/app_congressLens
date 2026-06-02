import json
from pathlib import Path

import bleach
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conference import Conference
from app.models.presentation import Presentation
from app.models.presentation_author import PresentationAuthor
from app.models.session import Session
from app.models.topic import Topic
from app.models.presentation_topic import presentation_topics
from app.importers.asco import ALLOWED_TAGS, ALLOWED_ATTRS, sanitize_html, strip_html, normalize_name
from app.importers.base import BaseImporter


class AACRImporter(BaseImporter):
    async def import_folder(self, conference_id: str, folder_path: str) -> dict:
        conference_uuid = conference_id
        conference = await self.db.get(Conference, conference_uuid)
        if not conference:
            return {"errors": ["Conference not found"], "imported_presentations": 0, "imported_sessions": 0, "imported_authors": 0, "skipped": 0}

        path = Path(folder_path)
        if not path.exists():
            return {"errors": ["Folder not found"], "imported_presentations": 0, "imported_sessions": 0, "imported_authors": 0, "skipped": 0}

        results = {"source": "aacr", "imported_presentations": 0, "imported_sessions": 0, "imported_authors": 0, "skipped": 0, "errors": []}

        for json_file in sorted(path.glob("**/*.json")):
            try:
                data = json.loads(json_file.read_text())
                await self._import_record(conference_uuid, data, results)
            except Exception as e:
                results["errors"].append(f"{json_file.name}: {str(e)}")
                results["skipped"] += 1

        await self.db.commit()
        return results

    async def _import_record(self, conference_uuid, data: dict, results: dict):
        session_id = await self._ensure_session(conference_uuid, data)

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

        pres = Presentation(**pres_data)
        self.db.add(pres)
        await self.db.flush()
        results["imported_presentations"] += 1

        await self._parse_authors(pres.id, data, results)
        await self._import_topics(pres.id, data)

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
        results_placeholder = None
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

    async def _import_topics(self, presentation_id, data: dict):
        raw_topics = []
        fields = data.get("AdditionalFields") or {}
        for key in ["Keywords", "Topic", "Category", "Track"]:
            vals = fields.get(key) or []
            if isinstance(vals, str):
                vals = [vals]
            raw_topics.extend(vals)

        for topic_name in raw_topics:
            name = topic_name.strip()
            if not name:
                continue
            norm = normalize_name(name)
            existing = await self.db.scalar(select(Topic).where(Topic.normalized_name == norm, Topic.type == "keyword"))
            if not existing:
                topic = Topic(name=name, normalized_name=norm, type="keyword")
                self.db.add(topic)
                await self.db.flush()
                existing = topic
            await self.db.execute(
                presentation_topics.insert().values(presentation_id=presentation_id, topic_id=existing.id)
            )