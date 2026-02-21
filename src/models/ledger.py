from sqlalchemy import Column, String, Boolean, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class Ledger(BaseEntity):
    """Ledger entity"""
    __tablename__ = "Ledgers"
    
    name = Column("Name", String(100), nullable=False)
    type = Column("Type", String(50), nullable=True)
    root_category = Column("RootCategory", String(50), nullable=True)
    code = Column("Code", String(50), nullable=True)
    address = Column("Address", String(200), nullable=True)
    city = Column("City", String(100), nullable=True)
    state = Column("State", String(50), nullable=True)
    zip_code = Column("ZipCode", String(20), nullable=True)
    country = Column("Country", String(100), nullable=True)
    
    # Shipping Address
    shipping_address = Column("ShippingAddress", String, nullable=True)
    shipping_city = Column("ShippingCity", String(100), nullable=True)
    shipping_state = Column("ShippingState", String(50), nullable=True)
    shipping_state_code = Column("ShippingStateCode", String(20), nullable=True)
    shipping_zip_code = Column("ShippingZipCode", String(20), nullable=True)
    shipping_country = Column("ShippingCountry", String(100), nullable=True)
    
    phone = Column("Phone", String(30), nullable=True)
    email = Column("Email", String(100), nullable=True)
    website = Column("Website", String(100), nullable=True)
    tax_id = Column("TaxId", String(50), nullable=True)
    is_group = Column("IsGroup", Boolean, default=False)
    is_registered = Column("IsRegistered", Boolean, nullable=True)
    
    # Tax-specific fields
    tax_class = Column("TaxClass", String(50), nullable=True)
    tax_rate = Column("TaxRate", Numeric(18, 2), nullable=True)
    is_credit_allowed = Column("IsCreditAllowed", Boolean, default=False)
    description = Column("Description", String(500), nullable=True)
    return_form_number = Column("ReturnFormNumber", String(50), nullable=True)
    
    tax_entity_id = Column("TaxEntityId", UUID(as_uuid=True), ForeignKey("Taxes.id"), nullable=True)
    receivable_ledger_id = Column("ReceivableLedgerId", UUID(as_uuid=True), nullable=True)
    payable_ledger_id = Column("PayableLedgerId", UUID(as_uuid=True), nullable=True)
    
    # Parent-Child relationship
    parent_id = Column("ParentId", UUID(as_uuid=True), ForeignKey("Ledgers.id"), nullable=True)
    
    # Company FK
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    company = relationship("Company", back_populates="ledgers")
    parent = relationship("Ledger", remote_side="Ledger.id", back_populates="children")
    children = relationship("Ledger", back_populates="parent")
    tax_entity = relationship("Tax", foreign_keys=[tax_entity_id])
    ledger_opening_balances = relationship("LedgerOpeningBalance", back_populates="ledger")
