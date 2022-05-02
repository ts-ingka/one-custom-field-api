from http import client
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api import crud, models, schemas
from api.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# not sure response_model is needed if we only have one model
# @app.post("/users/", response_model=schemas.User)
@app.post("/users", response_model=schemas.UserBase, status_code=201)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, client_id=user.client_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Client ID already exists")
    return crud.create_user(db=db, user=user)


@app.get("/users", response_model=list[schemas.UserBase])
def get_users(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@app.get("/user/{user_id}", response_model=schemas.UserBase)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, client_id=user_id)
    return db_user


@app.post("/datasources", response_model=schemas.DataSourceBase, status_code=201)
def create_datasource(datasource: schemas.DataSourceBase, db: Session = Depends(get_db)):
    db_datasource = crud.get_datasource(db=db, id=datasource.id)
    if db_datasource:
        raise HTTPException(status_code=400, detail="Datasource ID already exists")
    return crud.create_datasource(db=db, datasource=datasource)


@app.get("/datasources", response_model=list[schemas.DataSourceBase])
def get_datasources(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    db_datasources = crud.get_datasources(db=db, skip=skip, limit=limit)
    return db_datasources


@app.post("/load")
def populate_db(db: Session = Depends(get_db)):
    from api.models import User, DataSource, UserDatasource

    u1 = User(client_id="User1")
    u2 = User(client_id="User2")

    d1 = DataSource(id=1, description="Datasource 1!")
    d2 = DataSource(id=2, description="Datasource 2!")
    d3 = DataSource(id=3, description="Datasource 3!")

    db.add_all([u1, u2, d1, d2, d3])
    db.commit()

    ud1 = UserDatasource(datasource_id=d1.id, user_id=u1.client_id, can_modify_fields=False)
    ud2 = UserDatasource(datasource_id=d2.id, user_id=u2.client_id, can_modify_fields=False)
    ud3 = UserDatasource(datasource_id=d3.id, user_id=u1.client_id, can_modify_fields=False)
    ud4 = UserDatasource(datasource_id=d1.id, user_id=u2.client_id, can_modify_fields=False)

    db.add_all([ud1, ud2, ud3, ud4])
    db.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
