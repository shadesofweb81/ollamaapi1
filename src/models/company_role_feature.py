from sqlalchemy import Column, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid
from datetime import datetime

class CompanyRoleFeature(Base):
    """Company Role Feature entity"""
    __tablename__ = "CompanyRoleFeatures"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    can_create = Column("CanCreate", Boolean, default=False)
    can_read = Column("CanRead", Boolean, default=False)
    can_update = Column("CanUpdate", Boolean, default=False)
    can_delete = Column("CanDelete", Boolean, default=False)
    can_authorize = Column("CanAuthorize", Boolean, default=False)
    created_on = Column("CreatedOn", DateTime, default=datetime.utcnow)
    
    # Foreign keys
    role_id = Column("RoleId", UUID(as_uuid=True), ForeignKey("CompanyRoles.id"))
    feature_id = Column("FeatureId", UUID(as_uuid=True), ForeignKey("CompanyFeatures.id"))
    company_id = Column("CompanyId", UUID(as_uuid=True), ForeignKey("Companies.id"))
    
    # Relationships
    role = relationship("CompanyRole", back_populates="role_features")
    feature = relationship("CompanyFeature", back_populates="role_features")
