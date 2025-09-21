from typing import Optional
from sqlalchemy.orm import Session
from app.db.models.payment import Payment, PaymentMethod, PaymentStatusEnum
from app.schemas.payment import PaymentCreate, PaymentUpdateStatus
from datetime import datetime
from fastapi import HTTPException


def create_payment(db: Session, payment_data: PaymentCreate) -> Payment:
    payment = Payment(
        order_id=payment_data.order_id,
        payment_method_id=payment_data.payment_method_id,
        amount=payment_data.amount,
        currency=payment_data.currency,
        status=PaymentStatusEnum.pending,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment(db: Session, payment_id: int) -> Payment:
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def list_payments(db: Session, status: Optional[str] = None):
    query = db.query(Payment)
    if status:
        query = query.filter(Payment.status == status)
    return query.all()


def update_payment_status(db: Session, payment_id: int, status: PaymentUpdateStatus) -> Payment:
    payment = get_payment(db, payment_id)
    payment.status = status.status
    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


def cancel_payment(db: Session, payment_id: int) -> Payment:
    payment = get_payment(db, payment_id)
    if payment.status in [PaymentStatusEnum.cancelled, PaymentStatusEnum.refunded]:
        raise HTTPException(status_code=400, detail="Payment already cancelled or refunded")
    payment.status = PaymentStatusEnum.cancelled
    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


def refund_payment(db: Session, payment_id: int) -> Payment:
    payment = get_payment(db, payment_id)
    if payment.status != PaymentStatusEnum.completed:
        raise HTTPException(status_code=400, detail="Only completed payments can be refunded")
    payment.status = PaymentStatusEnum.refunded
    payment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment


def list_payment_methods(db: Session):
    return db.query(PaymentMethod).all()
