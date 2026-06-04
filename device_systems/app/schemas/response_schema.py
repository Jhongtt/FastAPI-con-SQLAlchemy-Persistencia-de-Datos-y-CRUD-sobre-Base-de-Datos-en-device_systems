from typing import Any, Optional
from pydantic import BaseModel


class StandardResponse(BaseModel):
    data: Any = None
    message: str = "Operation completed successfully"
    status_code: int = 200
