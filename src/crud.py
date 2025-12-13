from sqlalchemy.orm import Session
from . import models, schemas

# SSH Keys

def get_ssh_key(db: Session, ssh_key_id: int):
    return db.query(models.SSHKey).filter(models.SSHKey.id == ssh_key_id).first()

def get_ssh_key_by_name(db: Session, name: str):
    return db.query(models.SSHKey).filter(models.SSHKey.name == name).first()

def get_ssh_keys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SSHKey).offset(skip).limit(limit).all()

def create_ssh_key(db: Session, ssh_key: schemas.SSHKeyCreate):
    db_ssh_key = models.SSHKey(
        name=ssh_key.name,
        public_key=ssh_key.public_key,
        private_key=ssh_key.private_key, # In a real app, this would be encrypted
    )
    db.add(db_ssh_key)
    db.commit()
    db.refresh(db_ssh_key)
    return db_ssh_key

# Servers

def get_server(db: Session, server_id: int):
    return db.query(models.Server).filter(models.Server.id == server_id).first()

def get_server_by_hostname(db: Session, hostname: str):
    return db.query(models.Server).filter(models.Server.hostname == hostname).first()

def get_servers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Server).offset(skip).limit(limit).all()

def create_server(db: Session, server: schemas.ServerCreate):
    db_server = models.Server(
        hostname=server.hostname,
        ip_address=server.ip_address,
        username=server.username,
        password=server.password, # In a real app, this would be encrypted
        ssh_key_id=server.ssh_key_id,
    )
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

# Certificates

def get_certificate(db: Session, certificate_id: int):
    return db.query(models.Certificate).filter(models.Certificate.id == certificate_id).first()

def get_certificates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Certificate).offset(skip).limit(limit).all()

def create_certificate(db: Session, certificate: schemas.CertificateCreate):
    db_certificate = models.Certificate(**certificate.dict())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate
