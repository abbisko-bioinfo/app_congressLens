from app.importers.aacr import AACRImporter
from app.importers.asco import ASCOImporter

IMPORTERS = {
    "asco": ASCOImporter,
    "aacr": AACRImporter,
}
