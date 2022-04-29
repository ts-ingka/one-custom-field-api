from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, composite

from .database import Base


class DataSource(Base):
    __tablename__ = "datasources"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(2000))


class User(Base):
    __tablename__ = "users"

    client_id = Column(String(150), primary_key=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    permissions = relationship("UserPermission")


class UserPermission(Base):
    __tablename__ = "user_permissions"

    datasource_id = Column(
        Integer, ForeignKey("datasources.id"), primary_key=True
    )
    user_id = Column(
        String(150), ForeignKey("users.client_id"), primary_key=True
    )
    can_modify_fields = Column(Boolean, default=True, nullable=False)
    can_modify_values = Column(Boolean, default=True, nullable=False)
