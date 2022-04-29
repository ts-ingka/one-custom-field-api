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
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.client_id)
    if db_user:
        raise HTTPException(status_code=400, detail="Client ID already exists")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 1000):
    db_users = crud.get_users(db=db, skip=skip, limit=limit)
    return db_users


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
