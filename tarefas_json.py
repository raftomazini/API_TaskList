import json

def menu():
    print("1 - Consultar tarefas ativas")
    print("2 - Consultar tarefas concluídas")
    print("3 - Criar nova tarefa")
    print("4 - Alterar tarefa")
    print("5 - Excluir tarefa")
    print("0 - Sair")
    return input("Escolha sua opção: ")

def add_task(value):
    if taskList:
        new_id = max(task['id'] for task in taskList) + 1
    else:
        new_id = 0

    new_task = {
        'id': new_id,
        'descricao': value,
        'status': 'Em Andamento'
    }

    taskList.append(new_task)

def del_task(value):
    try:
        task_id = int(value)
    except ValueError:
        print("O ID informado deve ser um numero inteiro")
        return
    
    global taskList
    
    new_taskList = [task for task in taskList if task['id'] != task_id]

    if len(new_taskList) < len(taskList):
        taskList = new_taskList
        print("Exclusao realizada com sucesso!")
    else:
        print(f"Erro: Nao foi encontrada nenhuma tarefa com id {task_id}")

def show_active_task():
    for item in taskList:
        if item["status"] == 'Em Andamento':
            print(item)

def show_inactive_task():
    for item in taskList:
        if item["status"] == 'Concluido':
            print(item)

def show_tasks():
    for item in taskList:
        print(item)

def change_task(itemKey):
    print(f"Tarefa selecionada: {taskList[itemKey]}")
    new_description = input(f"Nova descrição (Deixe em branco para manter '{taskList[itemKey]['descricao']}'): ").strip()
    if new_description:
        taskList[itemKey]['descricao'] = new_description

    status = input("Alterar Estado (S/N): ")
    
    if status.upper().strip() == 'S':
        if taskList[itemKey]["status"] == "Em Andamento":
            taskList[itemKey]["status"] = 'Concluido'
        else:
            taskList[itemKey]["status"] = 'Em Andamento'
    
    print("Tarefa alterada.")

def load_tasks():
    try:
        with open(taskFile, "r") as file:
            return json.load(file)
        file.close()
    except Exception as e:
        print(f"Nao foi possivel abrir o arquivo {taskFile} - {e}")
        return []

def save_tasks():
    try:
        file = open(taskFile, "w+")
        json.dump(taskList, file, indent=4)        
        file.close()
    except Exception as e:
        print(f"Nao foi possivel abrir o arquivo {taskFile} - {e}")
        return []

def main():
    running = True
    while running:
        try:
          escolha = int(menu())
        except Exception:
            print("Informe uma opcao numerica")
            continue
        if escolha == 0:
            save_tasks()
            running = False
        elif escolha == 1:
            show_active_task()
        elif escolha == 2:
            show_inactive_task()
        elif escolha == 3:
            add_task(input("Digite a descricao da tarefa: "))
        elif escolha == 4:
            show_tasks()
            taskID = input("Informe o ID da tarafe: ")
            try:
                change_task(int(taskID))
            except Exception as e:
                print("O item deve ser um número")
        elif escolha == 5:
            show_tasks()
            del_task(input("Digite o codigo da tarefa que deseja excluir: "))

if __name__ == '__main__':
    taskFile = "taskFile.json"
    taskList = load_tasks()
    main()