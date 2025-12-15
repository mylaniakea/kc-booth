"""
Certificate rotation scheduler.

Automatically rotates certificates that are expiring within 30 days.

KNOWN ISSUES:
- Currently shares a single DB session across all job executions (see TODO below)
- Should create a new session for each job run to avoid stale connections

TODO:
- Fix DB session management to create new session per job
- Add proper error handling and alerting
- Make rotation threshold configurable (currently hardcoded to 30 days)
- Add metrics/monitoring for rotation success/failure
"""
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from . import crud, step_ca, distribution, schemas
from .logger import get_logger

logger = get_logger(__name__)


def rotate_certificates(db: Session) -> None:
    """
    Rotates certificates that are expiring within the next 30 days.
    
    This function:
    1. Queries all certificates
    2. Finds certificates expiring in < 30 days
    3. Issues new certificates via step-ca
    4. Stores new certificates in database
    5. Distributes certificates to servers (currently stub)
    
    TODO: This function currently uses a shared DB session passed from startup.
    Should be refactored to create a new session for each execution:
    
    ```python
    def rotate_certificates() -> None:
        from .database import SessionLocal
        db = SessionLocal()
        try:
            # rotation logic here
        finally:
            db.close()
    ```
    
    Args:
        db: Database session (currently shared, should be per-job)
    """
    try:
        logger.info("Starting certificate rotation job")
        certificates = crud.get_certificates(db)
        rotation_threshold = datetime.utcnow() + timedelta(days=30)
        rotated_count = 0
        
        for certificate in certificates:
            if certificate.expires_at < rotation_threshold:
                db_server = crud.get_server(db, certificate.server_id)
                if not db_server:
                    logger.warning(
                        f"Certificate {certificate.id} references non-existent "
                        f"server {certificate.server_id}, skipping"
                    )
                    continue
                
                try:
                    logger.info(f"Rotating certificate for {db_server.hostname}")
                    cert, key = step_ca.issue_certificate(db_server.hostname)
                    
                    expires_at = datetime.utcnow() + timedelta(days=90)
                    
                    new_certificate = schemas.CertificateCreate(
                        certificate=cert,
                        key=key,
                        expires_at=expires_at,
                        server_id=certificate.server_id,
                    )
                    crud.create_certificate(db, new_certificate)
                    
                    # Distribute to server (currently stub - logs warning)
                    distribution.distribute_certificate(db_server, cert, key)
                    
                    rotated_count += 1
                    logger.info(f"✓ Rotated certificate for {db_server.hostname}")
                    
                except Exception as e:
                    logger.error(
                        f"✗ Failed to rotate certificate for {db_server.hostname}: {e}",
                        exc_info=True
                    )
        
        logger.info(f"Certificate rotation complete. Rotated {rotated_count} certificates.")
        
    except Exception as e:
        logger.error(f"Certificate rotation job failed: {e}", exc_info=True)


def start_scheduler(db: Session) -> Optional[BackgroundScheduler]:
    """
    Starts the certificate rotation scheduler.
    
    Schedules certificate rotation to run daily at 2 AM.
    
    Args:
        db: Database session (passed to rotation job)
        
    Returns:
        BackgroundScheduler instance, or None if startup fails
    """
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            rotate_certificates,
            'interval',
            days=1,
            args=[db],
            id='certificate_rotation',
            name='Certificate Rotation',
            replace_existing=True
        )
        scheduler.start()
        logger.info("Certificate rotation scheduler started (runs daily)")
        return scheduler
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}", exc_info=True)
        return None
