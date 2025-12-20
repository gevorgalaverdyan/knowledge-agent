from datetime import datetime
from typing import List

from pydantic import BaseModel

class Chat(BaseModel):
    id: str
    messages: List[str]
    created_at: datetime
    updated_at: datetime