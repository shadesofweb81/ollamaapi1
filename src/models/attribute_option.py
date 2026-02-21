from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class AttributeOption(BaseEntity):
    """Attribute Option entity"""
    __tablename__ = "AttributeOptions"
    
    value = Column("Value", String(100), default="")
    display_name = Column("DisplayName", String(100), default="")
    description = Column("Description", String(500), default="")
    is_active = Column("IsActive", Boolean, default=True)
    sort_order = Column("SortOrder", Integer, default=0)
    
    # Foreign keys
    attribute_id = Column("AttributeId", UUID(as_uuid=True), ForeignKey("Attributes.id"))
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    attribute = relationship("Attribute", back_populates="attribute_options")
    product_attributes = relationship("ProductAttribute", back_populates="attribute_option")
    product_variant_attributes = relationship("ProductVariantAttribute", back_populates="attribute_option")
