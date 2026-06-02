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
    db: AsyncSession = Depends(get_db),
):
    importer_cls = IMPORTERS.get(source)
    if not importer_cls:
        raise HTTPException(400, f"Unknown importer source: {source}")
    importer = importer_cls(db)
    result = await importer.import_folder(conference_id, folder_path)
    return result