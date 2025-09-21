# app/api/v1/endpoints/payments.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.db.models.payment import Payment as PaymentModel, PaymentMethod as PaymentMethodModel

from app.schemas.payment import (
    PaymentCreate,
    PaymentMethodCreate,
    PaymentResponse,
    PaymentUpdateStatus,
    PaymentMethod,
)
from app.services import payment_service
from app.db.session import get_db

router = APIRouter()



@router.post("/methods", response_model=PaymentMethod)
def create_payment_method(data: PaymentMethodCreate, db: Session = Depends(get_db)):
    existing = db.query(PaymentMethodModel).filter_by(name=data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payment method already exists")

    method = PaymentMethodModel(name=data.name)
    db.add(method)
    db.commit()
    db.refresh(method)
    return method


@router.post("", response_model=PaymentResponse)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    payment = payment_service.create_payment(db, data)
    return payment


@router.get("/methods", response_model=List[PaymentMethod])
def list_payment_methods(db: Session = Depends(get_db)):
    return payment_service.list_payment_methods(db)


@router.get("", response_model=List[PaymentResponse])
def list_payments(status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return payment_service.list_payments(db, status)


@router.patch("/{payment_id}", response_model=PaymentResponse)
def update_payment_status(payment_id: int, data: PaymentUpdateStatus, db: Session = Depends(get_db)):
    return payment_service.update_payment_status(db, payment_id, data)


@router.post("/{payment_id}/cancel", response_model=PaymentResponse)
def cancel_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.cancel_payment(db, payment_id)


@router.post("/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.refund_payment(db, payment_id)


@router.get("/methods", response_model=List[PaymentMethod])
def list_payment_methods(db: Session = Depends(get_db)):
    return payment_service.list_payment_methods(db)


@router.post("/webhook")
def payment_webhook(payload: dict):
    # Implement your webhook logic here
    return {"message": "Webhook received"}


