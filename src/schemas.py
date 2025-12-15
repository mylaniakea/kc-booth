from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Union

class SSHKeyBase(BaseModel):
    name: str
    public_key: str

class SSHKeyCreate(SSHKeyBase):
    private_key: str

class SSHKey(SSHKeyBase):
    """SSH Key response model - private_key is excluded for security."""
    id: int
    model_config = ConfigDict(from_attributes=True)

class ServerBase(BaseModel):
    hostname: str
    ip_address: str
    username: str

class ServerCreate(ServerBase):
    password: str
    ssh_key_id: Union[int, None] = None

class Server(ServerBase):
    """Server response model - password is excluded for security."""
    id: int
    ssh_key_id: Union[int, None] = None
    model_config = ConfigDict(from_attributes=True)

class CertificateBase(BaseModel):
    certificate: str
    key: str

class CertificateCreate(CertificateBase):
    expires_at: datetime
    server_id: int

class Certificate(CertificateBase):
    id: int
    expires_at: datetime
    server_id: int
    model_config = ConfigDict(from_attributes=True)
