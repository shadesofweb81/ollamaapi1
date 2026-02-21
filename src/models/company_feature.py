from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models.base_entity import Base
import uuid
from datetime import datetime

class CompanyFeature(Base):
    """Company Feature entity"""
    __tablename__ = "CompanyFeatures"
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    name = Column("Name", String(100), default="")
    code = Column("Code", String(50), default="")
    description = Column("Description", String(500), default="")
    category = Column("Category", String(100), default="")
    is_system_feature = Column("IsSystemFeature", Boolean, default=False)
    is_enabled = Column("IsEnabled", Boolean, default=True)
    created_on = Column("CreatedOn", DateTime, default=datetime.utcnow)
    
    # Relationships
    role_features = relationship("CompanyRoleFeature", back_populates="feature")
