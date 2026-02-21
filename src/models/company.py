from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import BaseEntity

class Company(BaseEntity):
    """Company entity"""
    __tablename__ = "Companies"
    
    name = Column("Name", String(256), nullable=False)
    address = Column("Address", String(500), nullable=True)
    city = Column("City", String(100), nullable=True)
    state = Column("State", String(100), nullable=False)
    state_code = Column("StateCode", String(20), nullable=False)
    gstin = Column("GSTIN", String(50), nullable=False)
    zip_code = Column("ZipCode", String(20), nullable=True)
    country = Column("Country", String(100), nullable=False)
    phone = Column("Phone", String(30), nullable=True)
    email = Column("Email", String(256), nullable=False)
    website = Column("Website", String(256), nullable=True)
    tax_id = Column("TaxId", String(50), nullable=True)
    logo_url = Column("LogoUrl", String(500), nullable=False, default="")
    currency = Column("Currency", String(10), default="INR")
    starting_financial_year_date = Column("StartingFinancialYearDate", DateTime, nullable=True)
    
    # Bank Details
    bank_name = Column("BankName", String(256), nullable=True)
    account_number = Column("AccountNumber", String(50), nullable=True)
    ifsc_code = Column("IFSCCode", String(20), nullable=True)
    account_holder_name = Column("AccountHolderName", String(256), nullable=True)
    branch_name = Column("BranchName", String(256), nullable=True)
    swift_code = Column("SwiftCode", String(20), nullable=True)
    
    # Terms and Conditions
    terms_and_conditions = Column("TermsAndConditions", String, nullable=True)
    
    # Billing Address
    billing_address = Column("BillingAddress", String(500), nullable=True)
    billing_city = Column("BillingCity", String(100), nullable=True)
    billing_state = Column("BillingState", String(100), nullable=True)
    billing_state_code = Column("BillingStateCode", String(20), nullable=True)
    billing_zip_code = Column("BillingZipCode", String(20), nullable=True)
    billing_country = Column("BillingCountry", String(100), nullable=True)
    
    # Relationships
    user_companies = relationship("UserCompany", back_populates="company")
    products = relationship("Product", back_populates="company")
    ledgers = relationship("Ledger", back_populates="company")
    transactions = relationship("Transaction", back_populates="company")
    taxes = relationship("Tax", back_populates="company")
    transaction_type_settings = relationship("TransactionTypeSettings", back_populates="company")
    company_recharges = relationship("CompanyRecharge", back_populates="company")
    financial_years = relationship("FinancialYear", back_populates="company")
