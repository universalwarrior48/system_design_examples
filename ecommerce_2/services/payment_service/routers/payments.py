"""Payment service routers."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated
import uuid

from services.payment_service.database.session import get_db
from services.payment_service.models.payment import Payment, PaymentStatus
from services.payment_service.schemas.payment import (
    PaymentCreate,
    PaymentResponse,
    PaymentUpdate,
    RefundRequest
)
from shared.common.logging import get_logger

logger = get_logger("payment-service")

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    db: Annotated[Session, Depends(get_db)] = None
):
    """List all payments."""
    payments = db.query(Payment).offset(skip).limit(limit).all()
    return payments


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: uuid.UUID,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Get a specific payment by ID."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Process a new payment."""
    # Extract last 4 digits of card if provided
    card_last_four = None
    if payment_data.card_number:
        # Remove spaces and dashes
        clean_number = payment_data.card_number.replace(" ", "").replace("-", "")
        if len(clean_number) >= 4:
            card_last_four = clean_number[-4:]
    
    # Create the payment with PENDING status
    payment = Payment(
        order_id=payment_data.order_id,
        user_id=payment_data.user_id,
        amount=payment_data.amount,
        payment_method=payment_data.payment_method,
        card_last_four=card_last_four,
        status=PaymentStatus.PENDING
    )
    
    db.add(payment)
    db.flush()  # Get the payment ID
    
    # Generate a transaction ID (in real app, this would come from payment processor)
    payment.transaction_id = f"TXN-{payment.id.hex[:12].upper()}"
    
    db.commit()
    db.refresh(payment)
    
    logger.info(f"Created payment: {payment.id} for order: {payment.order_id}")
    return payment


@router.put("/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: uuid.UUID,
    payment_data: PaymentUpdate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Update an existing payment."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    # Update fields
    update_data = payment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    db.commit()
    db.refresh(payment)
    logger.info(f"Updated payment: {payment.id}")
    return payment


@router.patch("/{payment_id}/status", response_model=PaymentResponse)
async def update_payment_status(
    payment_id: uuid.UUID,
    status_update: PaymentUpdate,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Update payment status."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    if status_update.status:
        payment.status = status_update.status
    
    if status_update.transaction_id:
        payment.transaction_id = status_update.transaction_id
    
    db.commit()
    db.refresh(payment)
    logger.info(f"Updated payment {payment.id} status to: {payment.status}")
    return payment


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
async def refund_payment(
    payment_id: uuid.UUID,
    refund_request: RefundRequest,
    db: Annotated[Session, Depends(get_db)] = None
):
    """Process a refund for a payment."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    
    if payment.status != PaymentStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot refund payment with status: {payment.status}. Only completed payments can be refunded."
        )
    
    # Mark as refunded
    payment.status = PaymentStatus.REFUNDED
    
    db.commit()
    db.refresh(payment)
    logger.info(f"Refunded payment: {payment.id} - Reason: {refund_request.reason}")
    return payment
