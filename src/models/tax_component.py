from sqlalchemy import Column, String, Boolean, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class TaxComponent(BaseEntity):
    """Tax Component entity"""
    __tablename__ = "TaxComponents"
    
    name = Column("Name", String(100), nullable=False)
    description = Column("Description", String(500), default="")
    type = Column("Type", Integer, default=0)
    rate = Column("Rate", Numeric(18, 2), default=0)
    ledger_code = Column("LedgerCode", String(50), nullable=False)
    is_credit_allowed = Column("IsCreditAllowed", Boolean, default=False)
    return_form_number = Column("ReturnFormNumber", String(50), nullable=True)
    is_active = Column("IsActive", Boolean, default=True)
    
    # Foreign keys
    tax_id = Column("TaxId", UUID(as_uuid=True), ForeignKey("Taxes.id"))
    ledger_id = Column("LedgerId", UUID(as_uuid=True), ForeignKey("Ledgers.id"))
    receivable_ledger_id = Column("ReceivableLedgerId", UUID(as_uuid=True), nullable=True)
    payable_ledger_id = Column("PayableLedgerId", UUID(as_uuid=True), nullable=True)
    
    # Relationships
    tax = relationship("Tax", back_populates="components")
    ledger = relationship("Ledger")
