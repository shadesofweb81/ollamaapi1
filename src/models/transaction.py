from sqlalchemy import Column, String, Boolean, DateTime, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class Transaction(BaseEntity):
    """Transaction entity"""
    __tablename__ = "Transactions"
    
    transaction_number = Column("TransactionNumber", String(50), nullable=False)
    invoice_number = Column("InvoiceNumber", String(50), nullable=True)
    transaction_date = Column("TransactionDate", DateTime, nullable=False)
    form_type = Column("FormType", String(50), default="")
    type = Column("Type", Integer, nullable=False)
    journal_entry_type = Column("JournalEntryType", Integer, nullable=True)
    nature_of_transaction_types = Column("NatureOfTransactionTypes", Integer, nullable=True)
    due_date = Column("DueDate", DateTime)
    notes = Column("Notes", String(500), nullable=True)
    
    sub_total = Column("SubTotal", Numeric(18, 2), default=0)
    tax_rate = Column("TaxRate", Numeric(18, 2), default=0)
    tax_amount = Column("TaxAmount", Numeric(18, 2), default=0)
    discount = Column("Discount", Numeric(18, 2), default=0)
    discount_amount = Column("DiscountAmount", Numeric(18, 2), default=0)
    freight = Column("Freight", Numeric(18, 2), default=0)
    is_freight_included = Column("IsFreightIncluded", Boolean, default=False)
    round_off = Column("RoundOff", Numeric(18, 2), default=0)
    total = Column("Total", Numeric(18, 2), default=0)
    
    paid_amount = Column("PaidAmount", Numeric(18, 2), nullable=True)
    is_paid = Column("IsPaid", Boolean, default=False)
    status = Column("Status", Integer, default=0)
    payment_status = Column("PaymentStatus", Integer, default=0)
    reference_number = Column("ReferenceNumber", String(100), nullable=True)
    payment_method = Column("PaymentMethod", String(50), nullable=True)
    is_paid_with_transaction = Column("IsPaidWithTransaction", Boolean, default=False)
    
    # Foreign Keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"), nullable=True)
    financial_year_id = Column("FinancialYearId", UUID(as_uuid=True), ForeignKey("FinancialYears.id"), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="transactions")
    financial_year = relationship("FinancialYear")
    ledger_entries = relationship("TransactionLedger", back_populates="transaction")
    items = relationship("TransactionItem", back_populates="transaction")
    taxes = relationship("TransactionTax", back_populates="transaction")
    received_payments = relationship("TransactionPayment", foreign_keys="TransactionPayment.invoice_transaction_id", back_populates="invoice_transaction")
    payments_made = relationship("TransactionPayment", foreign_keys="TransactionPayment.payment_transaction_id", back_populates="payment_transaction")
