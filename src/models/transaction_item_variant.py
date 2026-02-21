from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid

class TransactionItemVariant(Base):
    """Transaction Item Variant entity"""
    __tablename__ = "TransactionItemVariants"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    transaction_item_id = Column("TransactionItemId", UUID(as_uuid=True), ForeignKey("TransactionItems.id"))
    product_variant_id = Column("ProductVariantId", UUID(as_uuid=True), ForeignKey("ProductVariants.id"))
    variant_code = Column("VariantCode", String(100), nullable=False)
    variant_name = Column("VariantName", String(256), nullable=False)
    quantity = Column("Quantity", Numeric(18, 4), default=0)
    unit_price = Column("UnitPrice", Numeric(18, 2), default=0)
    selling_price = Column("SellingPrice", Numeric(18, 2), default=0)
    current_quantity = Column("CurrentQuantity", Numeric(18, 4), default=0)
    serial_number = Column("SerialNumber", Integer, default=0)
    description = Column("Description", String(500), nullable=True)
    
    # Relationships
    transaction_item = relationship("TransactionItem", back_populates="variants")
    product_variant = relationship("ProductVariant")
