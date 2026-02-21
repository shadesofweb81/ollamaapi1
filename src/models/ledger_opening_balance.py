from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class LedgerOpeningBalance(BaseEntity):
    """Ledger Opening Balance entity"""
    __tablename__ = "LedgerOpeningBalances"
    
    opening_date = Column("OpeningDate", DateTime, nullable=False)
    opening_balance = Column("OpeningBalance", Numeric(18, 2), nullable=False)
    balance_type = Column("BalanceType", String(6), default="")
    
    # Foreign keys
    ledger_id = Column("LedgerId", UUID(as_uuid=True), ForeignKey("Ledgers.id"))
    financial_year_id = Column("FinancialYearId", UUID(as_uuid=True), ForeignKey("FinancialYears.id"))
    
    # Relationships
    ledger = relationship("Ledger", back_populates="ledger_opening_balances")
    financial_year = relationship("FinancialYear", back_populates="ledger_opening_balances")
