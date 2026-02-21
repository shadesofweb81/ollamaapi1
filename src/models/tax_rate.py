from sqlalchemy import Column, String, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class TaxRate(BaseEntity):
    """Tax Rate entity"""
    __tablename__ = "TaxRates"
    
    rate = Column("Rate", Numeric(18, 2), default=0)
    name = Column("Name", String(100), default="")
    hsn_code = Column("HSNCode", String(50), nullable=True)
    min_amount = Column("MinAmount", Numeric(18, 2), nullable=True)
    max_amount = Column("MaxAmount", Numeric(18, 2), nullable=True)
    effective_from = Column("EffectiveFrom", DateTime)
    effective_to = Column("EffectiveTo", DateTime, nullable=True)
    is_active = Column("IsActive", Boolean, default=True)
    
    # Foreign keys
    tax_id = Column("TaxId", UUID(as_uuid=True), ForeignKey("Taxes.id"))
    
    # Relationships
    tax = relationship("Tax", back_populates="rates")
