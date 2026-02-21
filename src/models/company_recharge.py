from sqlalchemy import Column, String, Boolean, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class CompanyRecharge(BaseEntity):
    """Company Recharge entity"""
    __tablename__ = "CompanyRecharges"
    
    amount = Column("Amount", Numeric(18, 2), nullable=False)
    period = Column("Period", Integer, nullable=False)
    start_date = Column("StartDate", DateTime, nullable=False)
    end_date = Column("EndDate", DateTime, nullable=False)
    recharge_status = Column("RechargeStatus", Integer, nullable=False)
    description = Column("Description", String(500), nullable=True)
    transaction_id = Column("TransactionId", String(100), nullable=True)
    payment_method = Column("PaymentMethod", String(50), nullable=True)
    paid_on = Column("PaidOn", DateTime, nullable=True)
    paid_by = Column("PaidBy", String(100), nullable=True)
    is_active = Column("IsActive", Boolean, default=True)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    company = relationship("Company", back_populates="company_recharges")
