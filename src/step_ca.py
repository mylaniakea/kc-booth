import subprocess
import os

def get_root_fingerprint():
    """
    Gets the root CA fingerprint.
    """
    command = ["step", "ca", "fingerprint"]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()

def issue_certificate(domain: str):
    """
    Issues a certificate for the given domain.
    """
    password = os.environ.get("STEP_PROVISIONER_PASSWORD")
    if not password:
        raise ValueError("STEP_PROVISIONER_PASSWORD environment variable not set.")

    command = [
        "step", "ca", "certificate", domain,
        f"{domain}.crt", f"{domain}.key",
        "--provisioner", "admin",
        "--provisioner-password", password,
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
