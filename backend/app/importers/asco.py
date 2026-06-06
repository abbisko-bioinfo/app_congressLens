import json
import re
from pathlib import Path

import bleach
from sqlalchemy import select

from app.importers.base import BaseImporter
from app.models.conference import Conference
from app.models.presentation import Presentation
from app.models.presentation_author import PresentationAuthor
from app.models.presentation_topic import presentation_topics
from app.models.session import Session
from app.models.topic import Topic

ALLOWED_TAGS = [
    "p", "br", "b", "strong", "i", "em", "u", "sup", "sub",
    "table", "thead", "tbody", "tr", "th", "td", "div", "span", "img",
]
ALLOWED_ATTRS = {"img": ["src", "alt"], "a": ["href"]}


def sanitize_html(raw: str | None) -> str | None:
    if not raw:
        return None
    return bleach.clean(
        raw,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        strip=True,
    )


def strip_html(raw: str | None) -> str | None:
    if not raw:
        return None
    return bleach.clean(raw, tags=[], strip=True)


def normalize_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.lower().strip())


class ASCOImporter(BaseImporter):
    async def import_folder(
        self, conference_id: str, folder_path: str, max_files: int = 0, offset: int = 0
    ) -> dict:
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
            "source": "asco",
            "imported_presentations": 0,
            "imported_sessions": 0,
            "imported_authors": 0,
            "skipped": 0,
            "errors": [],
        }

        skip_dirs = {"details"}

        batch = 0
        processed = 0
        skipped_offset = 0
        for json_file in sorted(path.glob("**/*.json")):
            if max_files and processed >= max_files:
                break
            if json_file.parent.name in skip_dirs:
                continue
            if skipped_offset < offset:
                skipped_offset += 1
                continue
            try:
                data = json.loads(json_file.read_text())
                content = data.get("data", {}).get("getContentById", {}).get("result", data)
                async with self.db.begin_nested():
                    await self._import_record(conference_uuid, content, results)
                batch += 1
                processed += 1
                if batch % 500 == 0:
                    await self.db.commit()
                    self.db.expire_all()
            except Exception as e:
                results["errors"].append(f"{json_file.name}: {str(e)}")
                results["skipped"] += 1

        await self.db.commit()
        return results

    async def _import_record(self, conference_uuid, content: dict, results: dict):
        session_id = await self._ensure_session(conference_uuid, content)
        pres_data = {
            "conference_id": conference_uuid,
            "session_id": session_id,
            "source_presentation_id": content.get("presentationId") or content.get("contentId"),
            "source_content_id": content.get("contentId"),
            "title": content.get("title", ""),
            "abstract_html": sanitize_html(content.get("body")),
            "abstract_text": strip_html(content.get("body")),
            "abstract_number": content.get("abstractNumber"),
            "poster_board_number": content.get("posterBoardNumber"),
            "clinical_trial_registry_number": content.get("clinicalTrialRegistryNumber"),
            "journal_citation": content.get("journalCitation"),
            "doi": content.get("doi"),
            "funding_sources": content.get("fundingSources") or [],
            "additional_funding_source": content.get("additionalFundingSource"),
            "source_url": content.get("presentationUrl"),
            "disclosure_url": content.get("disclosureUrl"),
            "has_abstract": bool(content.get("hasAbstract")),
            "has_slides": bool(content.get("hasSlides")),
            "has_posters": bool(content.get("hasPosters")),
            "has_videos": bool(content.get("hasVideos")),
        }

        if content.get("publishDate"):
            pd = content["publishDate"]
            pres_data["start_time"] = pd.get("start")
            pres_data["end_time"] = pd.get("end")
            pres_data["timezone"] = pd.get("timeZone")

        if content.get("firstAuthor"):
            fa = content["firstAuthor"]
            pres_data["first_author_name"] = fa.get("displayName")
        if content.get("presenter"):
            pres_data["presenter_name"] = content["presenter"].get("displayName")

        pres = Presentation(**pres_data)
        self.db.add(pres)
        await self.db.flush()
        results["imported_presentations"] += 1

        await self._import_authors(pres.id, content, results)
        await self._import_topics(pres.id, content)

    async def _ensure_session(self, conference_uuid, content: dict):
        source_session_id = content.get("sessionId")
        if not source_session_id:
            return None

        existing = await self.db.scalar(
            select(Session).where(
                Session.conference_id == conference_uuid,
                Session.source_session_id == str(source_session_id),
            )
        )
        if existing:
            # Update with richer metadata if available
            session_title = content.get("sessionTitle")
            if session_title:
                existing.title = session_title
            session_type = content.get("sessionType")
            if session_type:
                existing.session_type = session_type
            primary_track = content.get("primaryTrack")
            if isinstance(primary_track, dict) and primary_track.get("track"):
                existing.track = primary_track["track"]
            await self.db.flush()
            return existing.id

        # Extract track from primaryTrack dict
        track_name = None
        primary_track = content.get("primaryTrack")
        if isinstance(primary_track, dict) and primary_track.get("track"):
            track_name = primary_track["track"]

        session = Session(
            conference_id=conference_uuid,
            source_session_id=str(source_session_id),
            title=content.get("sessionTitle", ""),
            session_type=content.get("sessionType"),
            track=track_name,
        )
        self.db.add(session)
        await self.db.flush()
        return session.id

    async def _import_authors(self, presentation_id, content: dict, results: dict):
        authors = content.get("authors") or []
        for i, author in enumerate(authors):
            role = author.get("role", "")
            obj = PresentationAuthor(
                presentation_id=presentation_id,
                source_author_id=author.get("ascoId"),
                display_name=author.get("displayName", ""),
                normalized_name=normalize_name(author.get("displayName", "")),
                role=role,
                author_order=author.get("order") or i + 1,
                organization=author.get("publicationOrganization"),
                is_first_author=(role == "First Author"),
                is_presenter=(role == "Presenter"),
            )
            self.db.add(obj)
        await self.db.flush()
        results["imported_authors"] += len(authors)

    async def _import_topics(self, presentation_id, content: dict):
        raw_topic_names: list[str] = []

        # primaryTrack and subtrack are dicts {trackId, track} or {name, id}
        for field_name in ("primaryTrack", "subtrack"):
            val = content.get(field_name)
            if isinstance(val, dict):
                track_name = val.get("track") or val.get("name") or ""
                if track_name.strip():
                    raw_topic_names.append(track_name.strip())
            elif isinstance(val, str) and val.strip():
                raw_topic_names.append(val.strip())

        # tracks is a list of dicts or strings
        for track in content.get("tracks") or []:
            if isinstance(track, dict):
                tn = track.get("track") or track.get("name") or ""
                if tn.strip():
                    raw_topic_names.append(tn.strip())
            elif isinstance(track, str) and track.strip():
                raw_topic_names.append(track.strip())

        seen_norms: set[str] = set()
        for name in raw_topic_names:
            if not name:
                continue
            norm = normalize_name(name)
            if norm in seen_norms:
                continue
            seen_norms.add(norm)

            existing = await self.db.scalar(
                select(Topic).where(
                    Topic.normalized_name == norm, Topic.type == "track"
                )
            )
            if not existing:
                topic = Topic(name=name, normalized_name=norm, type="track")
                self.db.add(topic)
                await self.db.flush()
                existing = topic

            from sqlalchemy.dialects.postgresql import insert as pg_insert

            await self.db.execute(
                pg_insert(presentation_topics)
                .values(presentation_id=presentation_id, topic_id=existing.id)
                .on_conflict_do_nothing()
            )
