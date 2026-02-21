from sqlalchemy import Column, String, Boolean, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid

class TransactionLedger(Base):
    """Transaction Ledger entity"""
    __tablename__ = "TransactionLedgers"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    serial_number = Column("SerialNumber", Integer, default=0)
    transaction_id = Column("TransactionId", UUID(as_uuid=True), ForeignKey("Transactions.id"))
    ledger_id = Column("LedgerId", UUID(as_uuid=True), ForeignKey("Ledgers.id"))
    type = Column("Type", Integer, nullable=False)
    amount = Column("Amount", Numeric(18, 2), default=0)
    description = Column("Description", String(500), nullable=True)
    is_main_entry = Column("IsMainEntry", Boolean, nullable=True)
    is_system_entry = Column("IsSystemEntry", Boolean, nullable=True)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="ledger_entries")
    ledger = relationship("Ledger")
