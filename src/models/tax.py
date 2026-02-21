from sqlalchemy import Column, String, Boolean, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class Tax(BaseEntity):
    """Tax entity"""
    __tablename__ = "Taxes"
    
    name = Column("Name", String(100), nullable=False)
    description = Column("Description", String(500), default="")
    category = Column("Category", Integer, default=0)
    is_active = Column("IsActive", Boolean, default=True)
    is_composite = Column("IsComposite", Boolean, default=False)
    default_rate = Column("DefaultRate", Numeric(18, 2), default=0)
    hsn_code = Column("HSNCode", String(50), nullable=True)
    section_code = Column("SectionCode", String(50), nullable=True)
    is_reverse_charge_applicable = Column("IsReverseChargeApplicable", Boolean, default=False)
    is_deductible_at_source = Column("IsDeductibleAtSource", Boolean, default=False)
    is_collected_at_source = Column("IsCollectedAtSource", Boolean, default=False)
    return_form_number = Column("ReturnFormNumber", String(50), nullable=True)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    company = relationship("Company", back_populates="taxes")
    components = relationship("TaxComponent", back_populates="tax")
    rates = relationship("TaxRate", back_populates="tax")
