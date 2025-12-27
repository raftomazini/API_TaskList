import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
from services.models import Tasks, modTask, addTask, getUsers, addUsers
from services import task_services, user_services, security
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Validação de token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    valid_token = security.check_token(token)
    if valid_token == -1:
        raise HTTPException(status_code=401, detail="Token expirado")
    elif not valid_token:
        raise HTTPException(status_code=401, detail="Token inválido")
    else:
        return valid_token

# Rotas para tarefas
#
# Rotas para listar todas as tarefas
@app.get("/tasks", response_model=list[Tasks])
async def get_all_tasks(user: Annotated[dict, Depends(get_current_user)]):
    return await task_services.get_all_tasks(user['id'])

# Rota para listar apenas as tarefas ativas
@app.get("/tasks/actives", response_model=list[Tasks])
async def get_active_tasks(user: Annotated[dict, Depends(get_current_user)]):
    return await task_services.get_active_tasks(user['id'])

# Rota para listar apenas as tarefas inativas
@app.get("/tasks/inactives", response_model=list[Tasks])
async def get_inactive_tasks(user: Annotated[dict, Depends(get_current_user)]):
    return await task_services.get_inactive_tasks(user['id'])

# Rota para listar uma tarefa especifica
@app.get("/tasks/{task_id}", response_model=Tasks)
async def get_task_by_id(task_id: int, user: Annotated[dict, Depends(get_current_user)]):
    task = await task_services.get_task_by_id(task_id, user['id'])
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    elif task is False:
        raise HTTPException(status_code=500, detail="Database Error")
    return task

# Rota para adicionar uma tarefa nova
@app.post("/tasks", response_model=Tasks)
async def add_task(params: addTask, user: Annotated[dict, Depends(get_current_user)]):
    tasks = await task_services.add_task(params.description, user['id'])
    if tasks:
        return tasks
    else:
        raise HTTPException(status_code=404, detail=f"Problems adding a new Task {params.description}")

# Rota para excluir uma tarefa especifica
@app.delete("/tasks/{task_id}")
async def del_task_by_id(task_id: int, user: Annotated[dict, Depends(get_current_user)]):
    wasDeleted = await task_services.del_task_by_id(task_id, user['id'])
    if wasDeleted == -1:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    elif not wasDeleted:
        raise HTTPException(status_code=404, detail=f"Error excluding task with ID {task_id}")
    # Retorna status 204 (No Content) para DELETE bem-sucedido
    return {"message": f"Tasks ID {task_id} successfully excluded"}
    
# Rota para alterar uma tarefa especifica
@app.patch("/tasks/{task_id}", response_model=Tasks)
async def change_task(task_id: int, params: modTask, user: Annotated[dict, Depends(get_current_user)]):
    tasks = await task_services.change_task(task_id, params.description, params.active, user['id'])
    if tasks is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    elif tasks is False:
        raise HTTPException(status_code=500, detail="Database Error")
    return tasks

# Rotas para usuários
#
# Rota para listar uma usuário especifico por username
@app.get("/user/", response_model=getUsers)
async def get_user_by_id(user: Annotated[dict, Depends(get_current_user)]):
    user = await user_services.get_user_by_id(user['id'])
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with USERNAME {user['username']} not found")
    elif user is False:
        raise HTTPException(status_code=500, detail="Database Error")
    return user

# Rota para registar novo usuário
@app.post("/user/register/", response_model=getUsers)
async def add_user(params: addUsers):
    user = await user_services.add_user(params.username, params.password)
    if user == -1:
        raise HTTPException(status_code=409, detail=f"Trying to add an user that already exists {params.username}")
    elif user == False:
        raise HTTPException(status_code=404, detail=f"Problems adding a new User {params.username}")
    else:
        return user

# Rota para alterar a senha
@app.patch("/user/", response_model=getUsers)
async def add_user(params: addUsers, user: Annotated[dict, Depends(get_current_user)]):
    user = await user_services.change_user(id=user['id'], username=params.username, password=params.password)
    if user == None:
        raise HTTPException(status_code=404, detail=f"Trying to change an user that not exists {params.username}")
    elif user == -1:
        raise HTTPException(status_code=500, detail=f"Username problably alread existis {params.username}")
    elif user == False:
        raise HTTPException(status_code=404, detail=f"Problems changing an User {params.username}")
    else:
        return user


# Rota para validar usuário e obter token 
@app.post("/token/")
async def get_token(params: addUsers):
    token = await security.token(username=params.username, password=params.password)
    if token:
        return token
    else:
        raise HTTPException(status_code=404, detail="Erro ao validar usuario/senha")

# Handler para tratar erros 500 (internos) que não são HTTPException
@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )
    
# Rodar a api
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

