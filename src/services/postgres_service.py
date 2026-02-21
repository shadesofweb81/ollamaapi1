from typing import List, Optional, Type, TypeVar, Generic
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models.base_entity import Base

T = TypeVar('T', bound=Base)

class PostgresService(Generic[T]):
    """Generic PostgreSQL service for CRUD operations"""
    
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination"""
        query = select(self.model).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
    
    async def get_by_id(self, session: AsyncSession, id: UUID) -> Optional[T]:
        """Get a record by ID"""
        query = select(self.model).where(self.model.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_company_id(self, session: AsyncSession, company_id: UUID, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records for a specific company"""
        if hasattr(self.model, 'company_id'):
            query = select(self.model).where(self.model.company_id == company_id).offset(skip).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()
        return []
    
    # Sync versions
    def get_all_sync(self, session: Session, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records with pagination (sync)"""
        return session.query(self.model).offset(skip).limit(limit).all()
    
    def get_by_id_sync(self, session: Session, id: UUID) -> Optional[T]:
        """Get a record by ID (sync)"""
        return session.query(self.model).filter(self.model.id == id).first()
    
    def get_by_company_id_sync(self, session: Session, company_id: UUID, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all records for a specific company (sync)"""
        if hasattr(self.model, 'company_id'):
            return session.query(self.model).filter(self.model.company_id == company_id).offset(skip).limit(limit).all()
        return []


# Service instances for each model
from models.company import Company
from models.ledger import Ledger
from models.transaction import Transaction
from models.transaction_item import TransactionItem
from models.transaction_ledger import TransactionLedger
from models.transaction_tax import TransactionTax
from models.transaction_payment import TransactionPayment
from models.product import Product
from models.product_variant import ProductVariant
from models.attribute import Attribute
from models.attribute_option import AttributeOption
from models.product_attribute import ProductAttribute
from models.product_variant_attribute import ProductVariantAttribute
from models.tax import Tax
from models.tax_component import TaxComponent
from models.tax_rate import TaxRate
from models.user_company import UserCompany
from models.transaction_type_settings import TransactionTypeSettings
from models.company_recharge import CompanyRecharge
from models.financial_year import FinancialYear
from models.ledger_opening_balance import LedgerOpeningBalance
from models.product_opening_stock import ProductOpeningStock
from models.company_feature import CompanyFeature
from models.company_role import CompanyRole
from models.company_role_feature import CompanyRoleFeature

company_service = PostgresService(Company)
ledger_service = PostgresService(Ledger)
transaction_service = PostgresService(Transaction)
transaction_item_service = PostgresService(TransactionItem)
transaction_ledger_service = PostgresService(TransactionLedger)
transaction_tax_service = PostgresService(TransactionTax)
transaction_payment_service = PostgresService(TransactionPayment)
product_service = PostgresService(Product)
product_variant_service = PostgresService(ProductVariant)
attribute_service = PostgresService(Attribute)
attribute_option_service = PostgresService(AttributeOption)
product_attribute_service = PostgresService(ProductAttribute)
product_variant_attribute_service = PostgresService(ProductVariantAttribute)
tax_service = PostgresService(Tax)
tax_component_service = PostgresService(TaxComponent)
tax_rate_service = PostgresService(TaxRate)
user_company_service = PostgresService(UserCompany)
transaction_type_settings_service = PostgresService(TransactionTypeSettings)
company_recharge_service = PostgresService(CompanyRecharge)
financial_year_service = PostgresService(FinancialYear)
ledger_opening_balance_service = PostgresService(LedgerOpeningBalance)
product_opening_stock_service = PostgresService(ProductOpeningStock)
company_feature_service = PostgresService(CompanyFeature)
company_role_service = PostgresService(CompanyRole)
company_role_feature_service = PostgresService(CompanyRoleFeature)
