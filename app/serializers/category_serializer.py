from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CategoryCreateSerializer(BaseModel):
    name: str

class CategoryUpdateSerializer(BaseModel):
    name: Optional[str] = None

class CategoryResponseSerializer(BaseModel):
    id: UUID
    user_id: str
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True