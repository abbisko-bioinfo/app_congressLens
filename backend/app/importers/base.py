from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseImporter(ABC):
    def __init__(self, db: AsyncSession):
        self.db = db

    @abstractmethod
    async def import_folder(self, conference_id: str, folder_path: str) -> dict:
        pass