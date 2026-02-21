from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class FinancialYear(BaseEntity):
    """Financial Year entity"""
    __tablename__ = "FinancialYears"
    
    year_label = Column("YearLabel", String(20), nullable=False)
    start_date = Column("StartDate", DateTime, nullable=False)
    end_date = Column("EndDate", DateTime, nullable=False)
    is_active = Column("IsActive", Boolean, default=True)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    company = relationship("Company", back_populates="financial_years")
    ledger_opening_balances = relationship("LedgerOpeningBalance", back_populates="financial_year")
    product_opening_stocks = relationship("ProductOpeningStock", back_populates="financial_year")
