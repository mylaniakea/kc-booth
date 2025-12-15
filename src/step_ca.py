"""Step-CA integration for certificate management."""
import subprocess
import os
import re
from .config import get_settings


def validate_domain(domain: str) -> str:
    """
    Validate domain name to prevent command injection.
    
    Args:
        domain: Domain name to validate
        
    Returns:
        Validated domain name
        
    Raises:
        ValueError: If domain contains invalid characters
    """
    # Allow alphanumeric, dots, hyphens (standard domain characters)
    if not re.match(r'^[a-zA-Z0-9\.\-]+$', domain):
        raise ValueError(f"Invalid domain name: {domain}. Only alphanumeric, dots, and hyphens allowed.")
    if len(domain) > 253:
        raise ValueError("Domain name too long")
    if domain.startswith('-') or domain.endswith('-'):
        raise ValueError("Domain cannot start or end with hyphen")
    return domain


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
        ValueError: If domain is invalid
        subprocess.CalledProcessError: If certificate issuance fails
    """
    # Validate domain to prevent command injection
    domain = validate_domain(domain)
    
    settings = get_settings()
    
    # Use validated domain in file paths
    cert_file = f"{domain}.crt"
    key_file = f"{domain}.key"
    
    command = [
        "step", "ca", "certificate", domain,
        cert_file, key_file,
        "--provisioner", "admin",
        "--provisioner-password", settings.step_provisioner_password,
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise e

    with open(cert_file, "r") as f:
        cert = f.read()
    with open(key_file, "r") as f:
        key = f.read()

    # Clean up temporary files
    os.remove(cert_file)
    os.remove(key_file)

    return cert, key
