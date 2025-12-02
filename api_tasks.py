from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import json

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

# Variaveis publicas
taskFile = "taskFile.json"
taskList = []
app = FastAPI()

# Funcao para carregar as taferas do arquivo
def load_tasks():
    try:
        with open(taskFile, "r") as file:
            return json.load(file)
        file.close()
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except:
        return []

# Funcao para gravar as tarefas no arquivo
def save_tasks():
    try:
        file = open(taskFile, "w+")
        json.dump(taskList, file, indent=4)        
        file.close()
    except Exception as e:
        return []

# Carrega a lista de taferas
taskList = load_tasks()

# Rotas da API
# Rotas para listar todas as tarefas
@app.get("/tasks", response_model=list[Tasks])

def get_all_tasks():
    return taskList

# Rota para listar apenas as tarefas ativas
@app.get("/tasks/actives", response_model=list[Tasks])

def get_active_tasks():
    return [task for task in taskList if task['status'] == 'Em Andamento']

# Rota para listar apenas as tarefas inativas
@app.get("/tasks/inactives", response_model=list[Tasks])

def get_inactive_tasks():
    return [task for task in taskList if task['status'] == "Concluido"]

# Rota para listar uma tarefa especifica
@app.get("/tasks/{task_id}", response_model=Tasks)

def get_task_by_id(task_id: int):
    for task in taskList:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Item not found")

# Rota para adicionar uma tarefa nova
@app.post("/tasks")

def add_task(params: addTask):
    if taskList:
        new_id = max(task['id'] for task in taskList) + 1
    else:
        new_id = 0

    new_task = {
        'id': new_id,
        'description': params.description,
        'status': 'Em Andamento'
    }
    taskList.append(new_task)
    save_tasks()
    return taskList

# Rota para excluir uma tarefa especifica
@app.delete("/tasks/{value}", response_model=list[Tasks])

def del_task_by_id(value: int):
    try:
        task_id = int(value)
    except ValueError:
        print("O ID informado deve ser um numero inteiro")
        return
    
    global taskList
    
    new_taskList = [task for task in taskList if task['id'] != task_id]

    if len(new_taskList) < len(taskList):
        taskList = new_taskList
        save_tasks()
        return taskList
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
# Rota para alterar uma tarefa especifica
@app.patch("/tasks/{id}")

def change_task(id: int, params: modTask):
    task_id = id
    new_description = params.description
    new_status = params.status
    
    # Busca o índice (posição) da tarefa na lista, usando o ID
    try:
        # Encontra o índice do primeiro item onde o ID corresponde
        idx = next(i for i, task in enumerate(taskList) if task["id"] == task_id)
    except StopIteration:
        # Se o 'next' não encontrar nada, lança 404
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    
    try:
        if new_description:
            taskList[idx]['description'] = new_description

        old_status = taskList[idx]["status"]
        if new_status in ('Em Andamento', 'Concluido'):
            if new_status != old_status:
                taskList[idx]["status"] = new_status
                
        try:
            save_tasks()
            return taskList[idx]
        except:
            raise HTTPException(status_code=404, detail="Problem saving task")
    except:
        raise HTTPException(status_code=404, detail="Item not found")

# Rodar a api
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
