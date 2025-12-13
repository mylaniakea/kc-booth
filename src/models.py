import sqlalchemy
from .database import metadata

servers = sqlalchemy.Table(
    "servers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("hostname", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("ip_address", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("password", sqlalchemy.String), # Will be encrypted
    sqlalchemy.Column("ssh_key_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("ssh_keys.id")),
)

ssh_keys = sqlalchemy.Table(
    "ssh_keys",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True, index=True),
    sqlalchemy.Column("public_key", sqlalchemy.String, unique=True),
    sqlalchemy.Column("private_key", sqlalchemy.String), # Will be encrypted
)
