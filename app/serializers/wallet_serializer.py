from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class WalletCreateSerializer(BaseModel):
    name: str
    balance: Optional[float] = 0.0

class WalletUpdateSerializer(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None

class WalletResponseSerializer(BaseModel):
    id: UUID
    user_id: str
    name: str
    balance: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True