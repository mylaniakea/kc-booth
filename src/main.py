from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/ssh-keys/", response_model=schemas.SSHKey)
def create_ssh_key(ssh_key: schemas.SSHKeyCreate, db: Session = Depends(get_db)):
    db_ssh_key = crud.get_ssh_key_by_name(db, name=ssh_key.name)
    if db_ssh_key:
        raise HTTPException(status_code=400, detail="SSH key with this name already exists")
    return crud.create_ssh_key(db=db, ssh_key=ssh_key)

@app.get("/ssh-keys/", response_model=List[schemas.SSHKey])
def read_ssh_keys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ssh_keys = crud.get_ssh_keys(db, skip=skip, limit=limit)
    return ssh_keys

@app.get("/ssh-keys/{ssh_key_id}", response_model=schemas.SSHKey)
def read_ssh_key(ssh_key_id: int, db: Session = Depends(get_db)):
    db_ssh_key = crud.get_ssh_key(db, ssh_key_id=ssh_key_id)
    if db_ssh_key is None:
        raise HTTPException(status_code=404, detail="SSH key not found")
    return db_ssh_key

@app.get("/")
async def read_root():
    return {"message": "Welcome to kc-booth"}
