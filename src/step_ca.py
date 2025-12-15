"""Step-CA integration for certificate management."""
import subprocess
import os
from .config import get_settings


def get_root_fingerprint() -> str:
    """
    Gets the root CA fingerprint.
    
    Returns:
        Root CA fingerprint string
    """
    command = ["step", "ca", "fingerprint"]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def issue_certificate(domain: str) -> tuple[str, str]:
    """
    Issues a certificate for the given domain.
    
    Args:
        domain: Domain name for the certificate
        
    Returns:
        Tuple of (certificate, private_key)
        
    Raises:
        subprocess.CalledProcessError: If certificate issuance fails
    """
    settings = get_settings()
    
    command = [
        "step", "ca", "certificate", domain,
        f"{domain}.crt", f"{domain}.key",
        "--provisioner", "admin",
        "--provisioner-password", settings.step_provisioner_password,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise e

    with open(f"{domain}.crt", "r") as f:
        cert = f.read()
    with open(f"{domain}.key", "r") as f:
        key = f.read()

    os.remove(f"{domain}.crt")
    os.remove(f"{domain}.key")

    return cert, key
