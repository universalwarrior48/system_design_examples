"""Payment schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from enum import Enum


class PaymentStatusEnum(str, Enum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentCreate(BaseModel):
    """Schema for creating a payment."""
    order_id: UUID
    user_id: UUID
    amount: float = Field(..., gt=0)
    payment_method: str  # e.g., "credit_card", "debit_card", "paypal"
    card_number: Optional[str] = None  # For card payments (last 4 digits extracted)
    card_expiry: Optional[str] = None  # MM/YY format
    card_cvv: Optional[str] = None  # CVV code


class PaymentResponse(BaseModel):
    """Schema for payment response."""
    id: UUID
    order_id: UUID
    user_id: UUID
    amount: float
    payment_method: str
    card_last_four: Optional[str]
    status: PaymentStatusEnum
    transaction_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentUpdate(BaseModel):
    """Schema for updating a payment."""
    status: Optional[PaymentStatusEnum] = None
    transaction_id: Optional[str] = None


class RefundRequest(BaseModel):
    """Schema for requesting a refund."""
    reason: str = Field(..., min_length=1)
    amount: Optional[float] = Field(None, gt=0)  # Partial refund amount (optional)
