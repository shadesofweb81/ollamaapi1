from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid

class UserCompany(Base):
    """User Company entity"""
    __tablename__ = "UserCompanies"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    user_id = Column("UserId", String(256), nullable=False)
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    role_id = Column("RoleId", UUID(as_uuid=True), ForeignKey("CompanyRoles.id"), nullable=True)
    role = Column("Role", String(50), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="user_companies")
    company_role = relationship("CompanyRole", back_populates="user_companies")
