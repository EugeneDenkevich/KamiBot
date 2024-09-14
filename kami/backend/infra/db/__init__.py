"""DB infrastructure"""

from kami.backend.infra.db.base import Base
from kami.backend.infra.db.tables.dialog import DialogTable

__all__ = ("Base", "DialogTable")
