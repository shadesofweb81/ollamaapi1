from sqlalchemy import Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class ProductAttribute(BaseEntity):
    """Product Attribute entity"""
    __tablename__ = "ProductAttributes"
    
    # Foreign keys
    product_id = Column("ProductId", UUID(as_uuid=True), ForeignKey("Products.id"))
    attribute_id = Column("AttributeId", UUID(as_uuid=True), ForeignKey("Attributes.id"))
    attribute_option_id = Column("AttributeOptionId", UUID(as_uuid=True), ForeignKey("AttributeOptions.id"), nullable=True)
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Additional properties
    is_active = Column("IsActive", Boolean, default=True)
    
    # Relationships
    product = relationship("Product", back_populates="product_attributes")
    attribute = relationship("Attribute", back_populates="product_attributes")
    attribute_option = relationship("AttributeOption", back_populates="product_attributes")
