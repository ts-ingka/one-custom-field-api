from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, client_id: str):
    return db.query(models.User).filter(models.User.client_id == client_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_datasource(db: Session, id: int):
    return db.query(models.DataSource).filter(models.DataSource.id == id).first()


def get_datasources(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.DataSource).offset(skip).limit(limit).all()


def create_datasource(db: Session, datasource: schemas.DataSourceBase):
    db_datasource = models.DataSource(**datasource.dict())
    db.add(db_datasource)
    db.commit()
    db.refresh(db_datasource)
    return db_datasource


# TODO: Add UserPermissions
# How would I add CRUD operations for UserPermissions?
# How would an update request look like?
