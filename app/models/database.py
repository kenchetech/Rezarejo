from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Text, Integer
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class PickupRecord(Base):
    __tablename__ = "pickup_records"
    pickup_id = Column(String(50), primary_key=True, index=True)
    agent_id = Column(String(50), index=True, nullable=False)
    supplier_phone = Column(String(20), nullable=False)
    station_code = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    gross_weight_kg = Column(Float, nullable=False)
    tare_weight_kg = Column(Float, nullable=False)
    net_weight_kg = Column(Float, nullable=False)
    unit_rate_ksh = Column(Float, nullable=False)
    total_payout_ksh = Column(Float, nullable=False)
    payout_method = Column(String(30), default="mpesa_b2c")
    receipt_number = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(String(30), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
    mpesa_transaction = relationship("MPesaTransactionRecord", back_populates="pickup", uselist=False)

class MPesaTransactionRecord(Base):
    __tablename__ = "mpesa_transactions"
    transaction_id = Column(String(50), primary_key=True, index=True)
    pickup_id = Column(String(50), ForeignKey("pickup_records.pickup_id"), nullable=False)
    conversation_id = Column(String(100), index=True)
    originator_conversation_id = Column(String(100))
    phone_number = Column(String(20), nullable=False)
    amount = Column(Float, nullable=False)
    result_code = Column(Integer, default=0)
    result_description = Column(Text)
    receiver_name = Column(String(150))
    completed_at = Column(DateTime, default=datetime.utcnow)
    pickup = relationship("PickupRecord", back_populates="mpesa_transaction")

class NemaTripClearanceRecord(Base):
    __tablename__ = "nema_trip_clearances"
    trip_id = Column(String(50), primary_key=True, index=True)
    driver_id = Column(String(50), index=True, nullable=False)
    vehicle_reg = Column(String(20), nullable=False)
    origin_hub_id = Column(String(50), nullable=False)
    destination_mrf_id = Column(String(50), nullable=False)
    estimated_weight_kg = Column(Float, nullable=False)
    nema_permit_number = Column(String(100), unique=True, index=True, nullable=False)
    qr_code_payload = Column(Text, nullable=False)
    inspection_passed = Column(Boolean, default=True)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
