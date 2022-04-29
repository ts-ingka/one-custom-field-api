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
@app.post("/users/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, client_id=user.client_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Client ID already exists")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


@app.post("/datasources/", response_model=schemas.DataSource, status_code=201)
def create_datasource(datasource: schemas.DataSource, db: Session = Depends(get_db)):
    db_datasource = crud.get_datasource(db=db, id=datasource.id)
    if db_datasource:
        raise HTTPException(status_code=400, detail="Datasource ID already exists")
    return crud.create_datasource(db=db, datasource=datasource)


@app.get("/datasources/", response_model=list[schemas.DataSource])
def get_datasources(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    db_datasources = crud.get_datasources(db=db, skip=skip, limit=limit)
    return db_datasources


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
