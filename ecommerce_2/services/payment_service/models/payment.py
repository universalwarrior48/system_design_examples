"""Payment database models."""
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from services.payment_service.database.session import Base


class PaymentStatus(str, PyEnum):
    """Payment status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    """Payment model."""
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)  # e.g., "credit_card", "debit_card", "paypal"
    card_last_four = Column(String(4))  # Last 4 digits of card (if applicable)
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    transaction_id = Column(String, unique=True, index=True)  # External payment processor transaction ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Payment(id={self.id}, order_id={self.order_id}, status={self.status})>"
