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
