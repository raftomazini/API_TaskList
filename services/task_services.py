import json
from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.exc import SQLAlchemyError
from . import database

# Função para obter as tarefas
def get_tasks(is_active: bool | None = None):
    stmt = select(database.dbtasks).order_by(database.dbtasks.c.id)
    if is_active != None:
        stmt = stmt.where(database.dbtasks.c.active == is_active)
    try:
        tasklist = []
        with database.engine.begin() as conn:
            result = conn.execute(stmt)
            for row in result:
                tasklist.append(row._asdict())
        
        return tasklist
    except SQLAlchemyError as e:
        print(f"Erro ao obter tarefas no banco de dados (todas/ativas/inativas): {e}")
        return False

# Função para obter todas as tarefas
def get_all_tasks():
    return get_tasks()

# Função para obter as tarefas ativas
def get_active_tasks():
    return get_tasks(True)

# Função para obter as tarefas concluidas
def get_inactive_tasks():
    return get_tasks(False)

# Função para obter a tarefa pelo ID
def get_task_by_id(task_id: int):
    try:
        stmt = select(database.dbtasks).where(database.dbtasks.c.id == task_id)
        with database.engine.begin() as conn:
            row = conn.execute(stmt).one_or_none()
            if row is None:
                return None
        return row._asdict()
    except SQLAlchemyError as e:
        print(f"Erro ao obter a tarefa pelo id: {e}")
        return False

# Função para adicionar uma nova tarefa
def add_task(description: str):
    try:
        stmt = insert(database.dbtasks).values(description=description, active=True).returning(database.dbtasks.c.id, 
                                                                                               database.dbtasks.c.description, 
                                                                                               database.dbtasks.c.active, 
                                                                                               database.dbtasks.c.created_at, 
                                                                                               database.dbtasks.c.updated_at)
        with database.engine.begin() as conn:
            result = conn.execute(stmt).one_or_none()
        
        if result is None:
            return None
        return result._asdict()
    except SQLAlchemyError as e:
        print(f"Erro ao adicionar uma nova tarefa no banco de dados: {e}")
        return False

# Função para excluir uma tarefa
def del_task_by_id(task_id: int):
    try:
        stmt = delete(database.dbtasks).where(database.dbtasks.c.id == task_id)
        with database.engine.begin() as conn:
            conn.execute(stmt)
        return True
    except SQLAlchemyError as e:
        print(f"Erro ao excluir uma tarefa no banco de dados: {e}")
        return False

# Função para alterar uma tarefa    
def change_task(task_id: int, description: str, active: bool):
    try:
        stmt = update(database.dbtasks).values(description=description, active=active, updated_at=func.now()).where(database.dbtasks.c.id == task_id)
        with database.engine.begin() as conn:
            conn.execute(stmt)
        # chamar a função para retornar a tarefa alterada
        return get_task_by_id(task_id)
    except SQLAlchemyError as e:
        print(f"Erro ao alterar uma tarefa no banco de dados: {e}")
        return False
