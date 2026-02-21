from sqlalchemy import Column, String, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid

class TransactionItem(Base):
    """Transaction Item entity"""
    __tablename__ = "TransactionItems"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    transaction_id = Column("TransactionId", UUID(as_uuid=True), ForeignKey("Transactions.id"))
    product_id = Column("ProductId", UUID(as_uuid=True), ForeignKey("Products.id"))
    description = Column("Description", String(500), nullable=False)
    quantity = Column("Quantity", Numeric(18, 4), default=0)
    unit_price = Column("UnitPrice", Numeric(18, 2), default=0)
    tax_rate = Column("TaxRate", Numeric(18, 2), default=0)
    tax_amount = Column("TaxAmount", Numeric(18, 2), default=0)
    discount_rate = Column("DiscountRate", Numeric(18, 2), default=0)
    discount_amount = Column("DiscountAmount", Numeric(18, 2), default=0)
    line_total = Column("LineTotal", Numeric(18, 2), default=0)
    current_quantity = Column("CurrentQuantity", Numeric(18, 4), default=0)
    serial_number = Column("SerialNumber", Integer, default=0)
    
    # Physical Stock fields
    system_quantity = Column("SystemQuantity", Numeric(18, 4), nullable=True)
    physical_quantity = Column("PhysicalQuantity", Numeric(18, 4), nullable=True)
    adjustment_reason = Column("AdjustmentReason", String(500), nullable=True)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    product = relationship("Product")
    variants = relationship("TransactionItemVariant", back_populates="transaction_item")
