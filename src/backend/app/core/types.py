from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, StringConstraints

from app.core.time import ensure_utc

NonEmptyStr = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]

# SQLite often returns naive datetimes; mark them UTC after parsing.
UtcDateTime = Annotated[datetime, AfterValidator(ensure_utc)]
