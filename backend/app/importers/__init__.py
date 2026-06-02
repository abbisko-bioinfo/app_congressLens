from app.importers.asco import ASCOImporter
from app.importers.aacr import AACRImporter

IMPORTERS = {
    "asco": ASCOImporter,
    "aacr": AACRImporter,
}