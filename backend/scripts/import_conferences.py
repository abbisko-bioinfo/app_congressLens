"""Bulk import script: creates Conferences and imports data for AACR-2025, AACR-2026, ASCO-2026.

Usage:
    cd backend && python -m scripts.import_conferences --data-root /data/attachmentFiles

Import order:
    1. Create Conference records
    2. AACR sessions (from session/ folder)
    3. AACR presentations (reference existing sessions)
    4. ASCO presentations (auto-create sessions from embedded data)
"""

import argparse
import asyncio
from pathlib import Path

from app.core.database import async_session_factory
from app.importers import IMPORTERS
from app.models.conference import Conference

CONFERENCES = [
    {
        "acronym": "AACR",
        "name": "AACR Annual Meeting 2025",
        "year": 2025,
        "start_date": "2025-04-27",
        "end_date": "2025-04-30",
        "location": "Chicago, IL",
        "timezone": "America/Chicago",
        "description": "American Association for Cancer Research Annual Meeting 2025",
    },
    {
        "acronym": "AACR",
        "name": "AACR Annual Meeting 2026",
        "year": 2026,
        "start_date": "2026-04-17",
        "end_date": "2026-04-22",
        "location": "San Diego, CA",
        "timezone": "America/Los_Angeles",
        "description": "American Association for Cancer Research Annual Meeting 2026",
    },
    {
        "acronym": "ASCO",
        "name": "ASCO Annual Meeting 2026",
        "year": 2026,
        "start_date": "2026-05-29",
        "end_date": "2026-06-03",
        "location": "Chicago, IL",
        "timezone": "America/Chicago",
        "description": "American Society of Clinical Oncology Annual Meeting 2026",
    },
]

DATA_SOURCES = [
    # (acronym, year, source_type, folder_name)
    ("AACR", 2025, "aacr", "AACR-2025"),
    ("AACR", 2026, "aacr", "AACR-2026"),
    ("ASCO", 2026, "asco", "ASCO-2026"),
]


async def ensure_conferences() -> dict[str, str]:
    """Create Conference records if they don't exist. Returns {key: id} mapping."""
    mapping: dict[str, str] = {}

    async with async_session_factory() as db:
        for conf_data in CONFERENCES:
            key = f"{conf_data['acronym']}-{conf_data['year']}"
            from sqlalchemy import select

            existing = await db.scalar(
                select(Conference).where(
                    Conference.acronym == conf_data["acronym"],
                    Conference.year == conf_data["year"],
                )
            )
            if existing:
                print(f"  [skip] {key} already exists: {existing.id}")
                mapping[key] = existing.id
            else:
                conference = Conference(**conf_data)
                db.add(conference)
                await db.flush()
                print(f"  [created] {key}: {conference.id}")
                mapping[key] = conference.id

        await db.commit()

    return mapping


async def import_data(data_root: str, mapping: dict[str, str]) -> None:
    """Import sessions first, then presentations for each data source."""
    for acronym, year, source_type, folder_name in DATA_SOURCES:
        key = f"{acronym}-{year}"
        conference_id = mapping.get(key)
        if not conference_id:
            print(f"  [warn] No conference found for {key}, skipping")
            continue

        folder_path = Path(data_root) / folder_name
        if not folder_path.exists():
            print(f"  [warn] Folder not found: {folder_path}, skipping")
            continue

        importer_cls = IMPORTERS[source_type]

        async with async_session_factory() as db:
            importer = importer_cls(db)

            # Step 1: Import sessions first (AACR only; ASCO auto-creates)
            if source_type == "aacr":
                print(f"  Importing sessions for {key}...")
                session_results = await importer.import_sessions_folder(
                    conference_id, str(folder_path)
                )
                print(
                    f"    Sessions: {session_results['imported_sessions']} imported, "
                    f"{session_results['skipped']} skipped"
                )
                await db.commit()

            # Step 2: Import presentations
            print(f"  Importing presentations for {key}...")
            pres_results = await importer.import_folder(conference_id, str(folder_path))
            print(
                f"    Presentations: {pres_results['imported_presentations']} imported, "
                f"Sessions: {pres_results['imported_sessions']}, "
                f"Authors: {pres_results['imported_authors']}, "
                f"Skipped: {pres_results['skipped']}"
            )
            if pres_results.get("errors"):
                for err in pres_results["errors"][:5]:
                    print(f"    [error] {err}")
                if len(pres_results["errors"]) > 5:
                    print(f"    ... and {len(pres_results['errors']) - 5} more errors")


async def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk import conference data")
    parser.add_argument(
        "--data-root",
        default="/data/attachmentFiles",
        help="Root directory containing AACR-2025/, AACR-2026/, ASCO-2026/ folders",
    )
    args = parser.parse_args()

    print("=== CongressLens Bulk Import ===\n")

    print("Step 1: Ensuring conference records...")
    mapping = await ensure_conferences()
    print(f"  {len(mapping)} conferences ready\n")

    print("Step 2: Importing data (sessions → presentations)...")
    await import_data(args.data_root, mapping)

    print("\n=== Import complete ===")


if __name__ == "__main__":
    asyncio.run(main())
