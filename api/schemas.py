from typing import Optional
from pydantic import BaseModel


class DataSourceBase(BaseModel):
    id: int
    description: Optional[str] = None

    # this is confusing a***
    can_modify_fields: Optional[bool]
    can_modify_values: Optional[bool]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    client_id: str
    is_active: bool = True
    is_admin: bool = False

    # this is confusing a***
    can_modify_fields: Optional[bool]
    can_modify_values: Optional[bool]

    class Config:
        orm_mode = True


class DataSourceSchema(DataSourceBase):
    users: list[UserBase]


class UserSchema(UserBase):
    datasources: list[DataSourceBase]


# class UserDatasourceBase(BaseModel):
#     datasource_id: int
#     user_id: str
#     can_modify_fields: bool = True
#     can_modify_values: bool = True

#     class Config:
#         orm_mode = True
