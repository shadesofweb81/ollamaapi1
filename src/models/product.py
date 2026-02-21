from sqlalchemy import Column, String, Boolean, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class Product(BaseEntity):
    """Product entity"""
    __tablename__ = "Products"
    
    product_code = Column("ProductCode", String(50), default="")
    name = Column("Name", String(256), nullable=False)
    description = Column("Description", String(500), default="")
    purchase_price = Column("PurchasePrice", Numeric(18, 2), default=0)
    selling_price = Column("SellingPrice", Numeric(18, 2), default=0)
    stock_quantity = Column("StockQuantity", Integer, default=0)
    is_active = Column("IsActive", Boolean, default=True)
    maintain_stock = Column("MaintainStock", Boolean, nullable=True)
    is_group = Column("IsGroup", Boolean, nullable=True)
    hsn_code = Column("HSNCode", String(50), default="")
    type = Column("Type", String(50), default="")
    sku = Column("SKU", String(100), default="")
    barcode = Column("Barcode", String(100), default="")
    unit = Column("Unit", String(20), default="")
    
    # Hierarchical structure
    parent_id = Column("ParentId", UUID(as_uuid=True), ForeignKey("Products.id"), nullable=True)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    company = relationship("Company", back_populates="products")
    parent = relationship("Product", remote_side="Product.id", back_populates="children")
    children = relationship("Product", back_populates="parent")
    product_attributes = relationship("ProductAttribute", back_populates="product")
    product_variants = relationship("ProductVariant", back_populates="product")
    product_opening_stocks = relationship("ProductOpeningStock", back_populates="product")
