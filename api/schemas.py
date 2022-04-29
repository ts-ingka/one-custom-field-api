from typing import Optional
from pydantic import BaseModel


class DataSource(BaseModel):
    id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True


class UserPermission(BaseModel):
    datasource_id: int
    user_id: str
    can_modify_fields: bool = True
    can_modify_values: bool = True

    class Config:
        orm_mode = True


class User(BaseModel):
    client_id: str
    is_active: bool = True
    is_admin: bool = False
    permissions: list[UserPermission] = []

    class Config:
        orm_mode = True
