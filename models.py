from pydantic import BaseModel

# Modelo de dados
class Tasks(BaseModel):
    id: int
    description: str
    status: str

# Modelo para entrada de dados
class addTask(BaseModel):
    description: str

# Modelo para alteracao de dados
class modTask(BaseModel):
    description: str
    status: str
