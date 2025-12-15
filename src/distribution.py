"""
Certificate distribution module.

Handles distributing certificates to remote servers via SSH.

TODO: This module is currently a stub and needs implementation.
For production use, implement actual SSH distribution using paramiko or fabric.
"""
from typing import Any
from .logger import get_logger

logger = get_logger(__name__)


def distribute_certificate(server: Any, certificate: str, key: str) -> None:
    """
    Distributes a certificate to a server via SSH.
    
    TODO: This is currently a stub implementation. For production use:
    1. Install paramiko or fabric: pip install paramiko
    2. Implement SSH connection using server.username, server.ip_address
    3. Use server.password or ssh_key for authentication
    4. Copy certificate and key to appropriate locations on remote server
    5. Reload/restart relevant services (e.g., nginx, apache)
    6. Add error handling and retry logic
    
    Args:
        server: Server model instance with connection details
        certificate: PEM-encoded certificate content
        key: PEM-encoded private key content
        
    Raises:
        NotImplementedError: Always raised as this is a stub
        
    Example implementation:
        ```python
        import paramiko
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server.ip_address,
            username=server.username,
            password=server.password
        )
        
        # Upload certificate
        sftp = ssh.open_sftp()
        sftp.put_file('/tmp/cert.pem', '/etc/ssl/certs/server.pem')
        sftp.put_file('/tmp/key.pem', '/etc/ssl/private/server.key')
        sftp.close()
        
        # Reload service
        stdin, stdout, stderr = ssh.exec_command('systemctl reload nginx')
        ssh.close()
        ```
    """
    logger.warning(
        f"Certificate distribution stub called for {server.hostname}. "
        "This is not implemented. Certificate will not be deployed to remote server."
    )
    logger.debug(f"Certificate length: {len(certificate)} bytes")
    logger.debug(f"Key length: {len(key)} bytes")
    
    # For now, just log that we would distribute
    # In production, this should raise NotImplementedError or implement actual distribution
    logger.info(f"TODO: Implement actual certificate distribution for {server.hostname}")
