from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class ProductVariantAttribute(BaseEntity):
    """Product Variant Attribute entity"""
    __tablename__ = "ProductVariantAttributes"
    
    # Foreign keys
    product_variant_id = Column("ProductVariantId", UUID(as_uuid=True), ForeignKey("ProductVariants.id"))
    attribute_id = Column("AttributeId", UUID(as_uuid=True), ForeignKey("Attributes.id"))
    attribute_option_id = Column("AttributeOptionId", UUID(as_uuid=True), ForeignKey("AttributeOptions.id"))
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Additional properties
    custom_value = Column("CustomValue", String(256), default="")
    is_active = Column("IsActive", Boolean, default=True)
    
    # Relationships
    product_variant = relationship("ProductVariant", back_populates="product_variant_attributes")
    attribute = relationship("Attribute")
    attribute_option = relationship("AttributeOption", back_populates="product_variant_attributes")
