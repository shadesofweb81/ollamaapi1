from sqlalchemy import Column, String, Boolean, Integer, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class ProductVariant(BaseEntity):
    """Product Variant entity"""
    __tablename__ = "ProductVariants"
    
    variant_code = Column("VariantCode", String(50), default="")
    name = Column("Name", String(256), nullable=False)
    description = Column("Description", String(500), default="")
    purchase_price = Column("PurchasePrice", Numeric(18, 2), default=0)
    selling_price = Column("SellingPrice", Numeric(18, 2), default=0)
    stock_quantity = Column("StockQuantity", Integer, default=0)
    min_stock_level = Column("MinStockLevel", Integer, default=0)
    max_stock_level = Column("MaxStockLevel", Integer, default=0)
    is_active = Column("IsActive", Boolean, default=True)
    sku = Column("SKU", String(100), default="")
    barcode = Column("Barcode", String(100), default="")
    weight = Column("Weight", Numeric(18, 4), default=0)
    unit = Column("Unit", String(20), default="")
    image_url = Column("ImageUrl", String(500), default="")
    sort_order = Column("SortOrder", Integer, default=0)
    
    # Foreign keys
    product_id = Column("ProductId", UUID(as_uuid=True), ForeignKey("Products.id"))
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    product = relationship("Product", back_populates="product_variants")
    product_variant_attributes = relationship("ProductVariantAttribute", back_populates="product_variant")
