from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class TransactionPayment(BaseEntity):
    """Transaction Payment entity"""
    __tablename__ = "TransactionPayments"
    
    payment_transaction_id = Column("PaymentTransactionId", UUID(as_uuid=True), ForeignKey("Transactions.id"))
    invoice_transaction_id = Column("InvoiceTransactionId", UUID(as_uuid=True), ForeignKey("Transactions.id"))
    payment_ledger_id = Column("PaymentLedgerId", UUID(as_uuid=True), ForeignKey("Ledgers.id"), nullable=True)
    amount = Column("Amount", Numeric(18, 2), default=0)
    payment_date = Column("PaymentDate", DateTime)
    
    # Relationships
    payment_transaction = relationship("Transaction", foreign_keys=[payment_transaction_id], back_populates="payments_made")
    invoice_transaction = relationship("Transaction", foreign_keys=[invoice_transaction_id], back_populates="received_payments")
    payment_ledger = relationship("Ledger")
