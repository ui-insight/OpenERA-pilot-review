"""SQLAlchemy ORM models.

Import all models here so they are registered with Base.metadata.
"""

from app.models.allowed_value import AllowedValue  # noqa: F401
from app.models.award import Award  # noqa: F401
from app.models.document import Document  # noqa: F401
from app.models.organization import Organization  # noqa: F401
from app.models.personnel import Personnel  # noqa: F401
from app.models.project import Project  # noqa: F401
from app.models.project_role import ProjectRole  # noqa: F401
from app.models.proposal import Proposal  # noqa: F401
