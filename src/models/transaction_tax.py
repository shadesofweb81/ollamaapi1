from sqlalchemy import Column, String, Boolean, Numeric, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid

class TransactionTax(Base):
    """Transaction Tax entity"""
    __tablename__ = "TransactionTaxes"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    transaction_id = Column("TransactionId", UUID(as_uuid=True), ForeignKey("Transactions.id"))
    tax_ledger_id = Column("TaxLedgerId", UUID(as_uuid=True), ForeignKey("Ledgers.id"))
    taxable_amount = Column("TaxableAmount", Numeric(18, 2), default=0)
    tax_amount = Column("TaxAmount", Numeric(18, 2), default=0)
    calculation_method = Column("CalculationMethod", String(50), default="ItemSubtotal")
    is_applied = Column("IsApplied", Boolean, default=False)
    applied_date = Column("AppliedDate", DateTime, nullable=True)
    reference_number = Column("ReferenceNumber", String(50), nullable=True)
    description = Column("Description", String(500), nullable=True)
    serial_number = Column("SerialNumber", Integer, default=0)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="taxes")
    tax_ledger = relationship("Ledger")
