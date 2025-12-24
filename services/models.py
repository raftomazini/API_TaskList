from pydantic import BaseModel
from datetime import datetime

# Modelo de dados para tasklist
class Tasks(BaseModel):
    id: int
    description: str
    active: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None

# Modelo para entrada de dados
class addTask(BaseModel):
    description: str

# Modelo para alteracao de dados
class modTask(BaseModel):
    description: str
    active: bool

# Modelo de dados para users
class Users(BaseModel):
    id: int
    username: str
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

# Modelo de dados para busca de users
class getUsers(BaseModel):
    id: int
    username: str
    created_at: datetime | None = None
    updated_at: datetime | None = None    

# Modelo de dados para adicionar users
class addUsers(BaseModel):
    username: str
    password: str
