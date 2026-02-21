from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class Attribute(BaseEntity):
    """Attribute entity"""
    __tablename__ = "Attributes"
    
    name = Column("Name", String(100), nullable=False)
    description = Column("Description", String(500), default="")
    is_required = Column("IsRequired", Boolean, default=False)
    is_active = Column("IsActive", Boolean, default=True)
    sort_order = Column("SortOrder", Integer, default=0)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    attribute_options = relationship("AttributeOption", back_populates="attribute")
    product_attributes = relationship("ProductAttribute", back_populates="attribute")
