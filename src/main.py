from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, step_ca
from .database import SessionLocal, engine
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SSH Keys

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

# Servers

@app.post("/servers/", response_model=schemas.Server)
def create_server(server: schemas.ServerCreate, db: Session = Depends(get_db)):
    db_server = crud.get_server_by_hostname(db, hostname=server.hostname)
    if db_server:
        raise HTTPException(status_code=400, detail="Server with this hostname already exists")
    return crud.create_server(db=db, server=server)

@app.get("/servers/", response_model=List[schemas.Server])
def read_servers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    servers = crud.get_servers(db, skip=skip, limit=limit)
    return servers

@app.get("/servers/{server_id}", response_model=schemas.Server)
def read_server(server_id: int, db: Session = Depends(get_db)):
    db_server = crud.get_server(db, server_id=server_id)
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    return db_server

# CA

@app.get("/ca/fingerprint")
def get_ca_fingerprint():
    return {"fingerprint": step_ca.get_root_fingerprint()}

@app.post("/ca/issue-certificate")
def issue_certificate_endpoint(server_id: int, db: Session = Depends(get_db)):
    db_server = crud.get_server(db, server_id=server_id)
    if db_server is None:
        raise HTTPException(status_code=404, detail="Server not found")
    
    cert, key = step_ca.issue_certificate(db_server.hostname)
    
    expires_at = datetime.utcnow() + timedelta(days=90) # Certificates are valid for 90 days
    
    certificate = schemas.CertificateCreate(
        certificate=cert,
        key=key,
        expires_at=expires_at,
        server_id=server_id,
    )
    crud.create_certificate(db, certificate)
    
    return {"certificate": cert, "key": key}

@app.get("/certificates/", response_model=List[schemas.Certificate])
def read_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    certificates = crud.get_certificates(db, skip=skip, limit=limit)
    return certificates

@app.get("/")
async def read_root():
    return {"message": "Welcome to kc-booth"}
