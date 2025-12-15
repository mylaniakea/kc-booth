"""Certificate rotation scheduler."""
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from . import crud, step_ca, distribution, schemas
from datetime import datetime, timedelta


def rotate_certificates(db: Session):
    """
    Rotates certificates that are expiring within the next 30 days.
    """
    certificates = crud.get_certificates(db)
    for certificate in certificates:
        if certificate.expires_at < datetime.utcnow() + timedelta(days=30):
            db_server = crud.get_server(db, certificate.server_id)
            if db_server:
                cert, key = step_ca.issue_certificate(db_server.hostname)
                
                expires_at = datetime.utcnow() + timedelta(days=90)
                
                new_certificate = schemas.CertificateCreate(
                    certificate=cert,
                    key=key,
                    expires_at=expires_at,
                    server_id=certificate.server_id,
                )
                crud.create_certificate(db, new_certificate)
                
                distribution.distribute_certificate(db_server, cert, key)
                
                print(f"Rotated certificate for {db_server.hostname}")


def start_scheduler(db: Session):
    """
    Starts the certificate rotation scheduler.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(rotate_certificates, 'interval', days=1, args=[db])
    scheduler.start()
