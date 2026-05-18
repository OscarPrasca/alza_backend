from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TagCreateSerializer(BaseModel):
    name: str

class TagUpdateSerializer(BaseModel):
    name: Optional[str] = None

class TagResponseSerializer(BaseModel):
    id: UUID
    user_id: str
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True