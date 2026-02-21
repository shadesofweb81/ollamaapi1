from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid
from datetime import datetime

class CompanyRole(Base):
    """Company Role entity"""
    __tablename__ = "CompanyRoles"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    name = Column("Name", String(100), default="")
    description = Column("Description", String(500), default="")
    is_system_role = Column("IsSystemRole", Boolean, default=False)
    created_on = Column("CreatedOn", DateTime, default=datetime.utcnow)
    modified_on = Column("ModifiedOn", DateTime, nullable=True)
    
    # Foreign keys
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    role_features = relationship("CompanyRoleFeature", back_populates="role")
    user_companies = relationship("UserCompany", back_populates="company_role")
