from pydantic import BaseModel

class SSHKeyBase(BaseModel):
    name: str
    public_key: str

class SSHKeyCreate(SSHKeyBase):
    private_key: str

class SSHKey(SSHKeyBase):
    id: int

    class Config:
        orm_mode = True

class ServerBase(BaseModel):
    hostname: str
    ip_address: str
    username: str

class ServerCreate(ServerBase):
    password: str
    ssh_key_id: int | None = None

class Server(ServerBase):
    id: int
    ssh_key_id: int | None = None

    class Config:
        orm_mode = True
