from pydantic import BaseModel, validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class TransactionCreateSerializer(BaseModel):
    title: str
    description: Optional[str] = None
    amount: float
    type: str
    wallet_id: UUID
    category_id: UUID
    tag_ids: Optional[List[UUID]] = []

    @validator("type")
    def validate_type(cls, v):
        if v not in ["expense", "income"]:
            raise ValueError("El tipo debe ser 'expense' o 'income'")
        return v

    @validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return v

class TransactionUpdateSerializer(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    type: Optional[str] = None
    wallet_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    tag_ids: Optional[List[UUID]] = None

class TransactionResponseSerializer(BaseModel):
    id: UUID
    user_id: str
    title: str
    description: Optional[str] = None
    amount: float
    type: str
    wallet_id: UUID
    category_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True