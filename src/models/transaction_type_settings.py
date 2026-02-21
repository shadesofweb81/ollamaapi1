from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class TransactionTypeSettings(BaseEntity):
    """Transaction Type Settings entity"""
    __tablename__ = "TransactionTypeSettings"
    
    transaction_type = Column("TransactionType", Integer, nullable=False)
    
    # Invoice Generation Settings
    auto_generate_invoice = Column("AutoGenerateInvoice", Boolean, default=True)
    allow_duplicate_invoice_number = Column("AllowDuplicateInvoiceNumber", Boolean, default=False)
    
    # Address Display Settings
    show_billing_address = Column("ShowBillingAddress", Boolean, default=True)
    show_shipping_address = Column("ShowShippingAddress", Boolean, default=True)
    require_billing_address = Column("RequireBillingAddress", Boolean, default=False)
    require_shipping_address = Column("RequireShippingAddress", Boolean, default=False)
    
    # Invoice Number Settings
    invoice_number_prefix = Column("InvoiceNumberPrefix", String(20), nullable=True)
    invoice_number_suffix = Column("InvoiceNumberSuffix", String(20), nullable=True)
    invoice_number_length = Column("InvoiceNumberLength", Integer, default=6)
    next_invoice_number = Column("NextInvoiceNumber", Integer, default=1)
    
    # Default address settings
    copy_billing_to_shipping = Column("CopyBillingToShipping", Boolean, default=False)
    copy_shipping_to_billing = Column("CopyShippingToBilling", Boolean, default=False)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    company = relationship("Company", back_populates="transaction_type_settings")
