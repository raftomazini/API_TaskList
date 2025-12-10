import json
from . import database

# Variaveis publicas
taskFile = "taskFile.json"
tasks = []

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
        json.dump(tasks, file, indent=4)        
        file.close()
    except Exception as e:
        return []

# Função para obter todas as tarefas
def get_all_tasks():
    return database.get_tasks()


# Função para obter as tarefas ativas
def get_active_tasks():
    return database.get_tasks(True)

# Função para obter as tarefas concluidas
def get_inactive_tasks():
    return database.get_tasks(False)

# Função para obter a tarefa pelo ID
def get_task_by_id(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task

# Função para adicionar uma nova tarefa
def add_task(description: str):
    execution = database.tasks_insert(description)
    if not execution:
        return False
    
    return execution

# Função para excluir uma tarefa
def del_task_by_id(task_id: int):
    global tasks

    oldLength = len(tasks)
    
    newTaskList = [task for task in tasks if task['id'] != task_id]

    if len(newTaskList) < len(oldLength):
        tasks = newTaskList
        save_tasks()
        return True
    else:
        return False

# Função para alterar uma tarefa    
def change_task(id: int, description: str, status: str):
    task_id = id
    new_description = description
    new_status = status
    
    # Busca o índice (posição) da tarefa na lista, usando o ID
    try:
        # Encontra o índice do primeiro item onde o ID corresponde
        idx = next(i for i, task in enumerate(tasks) if task["id"] == task_id)
    except StopIteration:
        # Se o 'next' não encontrar nada, lança 404
        return False
    
    try:
        if new_description:
            tasks[idx]['description'] = new_description

        old_status = tasks[idx]["status"]
        if new_status in ('Em Andamento', 'Concluido'):
            if new_status != old_status:
                tasks[idx]["status"] = new_status
                
        try:
            save_tasks()
            return tasks[idx]
        except:
            return False
    except:
        return False
    
# Carrega a lista de taferas
tasks = load_tasks()