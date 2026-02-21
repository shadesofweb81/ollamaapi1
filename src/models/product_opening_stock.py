from sqlalchemy import Column, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class ProductOpeningStock(BaseEntity):
    """Product Opening Stock entity"""
    __tablename__ = "ProductOpeningStocks"
    
    opening_date = Column("OpeningDate", DateTime, nullable=False)
    quantity = Column("Quantity", Numeric(18, 4), nullable=False)
    rate = Column("Rate", Numeric(18, 2), nullable=False)
    value_amount = Column("ValueAmount", Numeric(18, 2), default=0)
    
    # Foreign keys
    product_id = Column("ProductId", UUID(as_uuid=True), ForeignKey("Products.id"))
    financial_year_id = Column("FinancialYearId", UUID(as_uuid=True), ForeignKey("FinancialYears.id"))
    
    # Relationships
    product = relationship("Product", back_populates="product_opening_stocks")
    financial_year = relationship("FinancialYear", back_populates="product_opening_stocks")
