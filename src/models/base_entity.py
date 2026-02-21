from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class BaseEntity(Base):
    """Base entity with common fields"""
    __abstract__ = True
    
    id = Column("Id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, key="id")
    created_on = Column("CreatedOn", DateTime, default=datetime.utcnow)
    modified_on = Column("ModifiedOn", DateTime, nullable=True)
    created_by = Column("CreatedBy", String(256), default="")
    modified_by = Column("ModifiedBy", String(256), default="")
    authorized = Column("Authorized", Boolean, nullable=True, default=False)
    authorized_by = Column("AuthorizedBy", String(256), nullable=True)
    authorized_on = Column("AuthorizedOn", DateTime, nullable=True)
