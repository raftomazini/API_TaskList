from fastapi import FastAPI, HTTPException
from services.models import Tasks, modTask, addTask
from services import task_services
import uvicorn

app = FastAPI()

# Rotas para listar todas as tarefas
@app.get("/tasks", response_model=list[Tasks])
def get_all_tasks():
    return task_services.get_all_tasks()

# Rota para listar apenas as tarefas ativas
@app.get("/tasks/actives", response_model=list[Tasks])
def get_active_tasks():
    return task_services.get_active_tasks()

# Rota para listar apenas as tarefas inativas
@app.get("/tasks/inactives", response_model=list[Tasks])
def get_inactive_tasks():
    return task_services.get_inactive_tasks()

# Rota para listar uma tarefa especifica
@app.get("/tasks/{task_id}", response_model=Tasks)
def get_task_by_id(task_id: int):
    task = task_services.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    elif task is False:
        raise HTTPException(status_code=500, detail="Database Error")
    
    return task


# Rota para adicionar uma tarefa nova
@app.post("/tasks")
def add_task(params: addTask):
    tasks = task_services.add_task(params.description)
    if tasks:
        return tasks
    else:
        raise HTTPException(status_code=404, detail=f"Problems adding a new Task {params.description}")

# Rota para excluir uma tarefa especifica
@app.delete("/tasks/{task_id}")
def del_task_by_id(task_id: int):
    wasDeleted = task_services.del_task_by_id(task_id)
    if not wasDeleted:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    # Retorna status 204 (No Content) para DELETE bem-sucedido
    return {"message": "Tarefa excluída com sucesso"}
    
# Rota para alterar uma tarefa especifica
@app.patch("/tasks/{task_id}")
def change_task(task_id: int, params: modTask):
    tasks = task_services.change_task(task_id, params.description, params.active)

    if tasks is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    elif tasks is False:
        raise HTTPException(status_code=500, detail="Database Error")
    
    return tasks
    
# Rodar a api
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

