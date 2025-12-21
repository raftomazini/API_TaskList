from pydantic import BaseModel
#from typing import Optional
from datetime import datetime

# Modelo de dados
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
