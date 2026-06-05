from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.importers import IMPORTERS

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/conferences/{conference_id}/presentations")
async def import_presentations(
    conference_id: str,
    source: str,
    folder_path: str,
    max_files: int = 0,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    importer_cls = IMPORTERS.get(source)
    if not importer_cls:
        raise HTTPException(400, f"Unknown importer source: {source}")
    importer = importer_cls(db)
    result = await importer.import_folder(
        conference_id, folder_path, max_files=max_files, offset=offset
    )
    return result


@router.post("/conferences/{conference_id}/sessions")
async def import_sessions(
    conference_id: str,
    source: str,
    folder_path: str,
    max_files: int = 0,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    importer_cls = IMPORTERS.get(source)
    if not importer_cls:
        raise HTTPException(400, f"Unknown importer source: {source}")

    importer = importer_cls(db)

    if hasattr(importer, "import_sessions_folder"):
        result = await importer.import_sessions_folder(
            conference_id, folder_path, max_files=max_files, offset=offset
        )
        return result

    raise HTTPException(
        400,
        f"Source '{source}' does not support separate session import. "
        "Sessions are auto-created during presentation import.",
    )
