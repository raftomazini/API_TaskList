from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from . import database

# Função para obter as tarefas
async def get_tasks(user_id: int, is_active: bool | None = None):
    stmt = select(database.dbtasks).where(database.dbtasks.user_id == user_id).order_by(database.dbtasks.id)
    if is_active != None:
        stmt = stmt.where(database.dbtasks.active == is_active)
    try:
        tasklist = []
        async with database.async_session() as session:
            result = await session.execute(stmt)
            for row in result.scalars():
                tasklist.append(row.to_dict())
            return tasklist
    except SQLAlchemyError as e:
        print(f"Erro ao obter tarefas no banco de dados (todas/ativas/inativas): {e}")
        return False

# Função para obter todas as tarefas
async def get_all_tasks(user_id: int):
    return await get_tasks(user_id)

# Função para obter as tarefas ativas
async def get_active_tasks(user_id: int):
    return await get_tasks(user_id, True)

# Função para obter as tarefas concluidas
async def get_inactive_tasks(user_id: int):
    return await get_tasks(user_id, False)

# Função para obter a tarefa pelo ID
async def get_task_by_id(task_id: int, user_id: int):
    try:
        stmt = select(database.dbtasks).where(database.dbtasks.id == task_id, database.dbtasks.user_id == user_id)
        async with database.async_session() as session:
            result = await session.execute(stmt)
            data = result.scalar_one_or_none()
            return data.to_dict() if data else None
    except SQLAlchemyError as e:
        print(f"Erro ao obter a tarefa pelo id: {e}")
        return False

# Função para adicionar uma nova tarefa
async def add_task(description: str, user_id: int):
    try:
        task_obj = database.dbtasks(description=description, active=True, user_id=user_id)
        async with database.async_session() as session:
            async with session.begin():
                session.add(task_obj)
            await session.refresh(task_obj)
            return task_obj.to_dict()
    except SQLAlchemyError as e:
        print(f"Erro ao adicionar uma nova tarefa no banco de dados: {e}")
        return False

# Função para excluir uma tarefa
async def del_task_by_id(task_id: int, user_id: int):
    try:
        stmt = select(database.dbtasks).where(database.dbtasks.id == task_id, database.dbtasks.user_id == user_id)
        async with database.async_session() as session:
            async with session.begin():
                result = await session.execute(stmt)
                task_obj = result.scalar_one_or_none()
                if task_obj:
                    await session.delete(task_obj)
                else:
                    print(f"Tarefa ID {task_id} não encontrada")
                    return -1
            return True
    except SQLAlchemyError as e:
        print(f"Erro ao excluir uma tarefa no banco de dados: {e}")
        return False

# Função para alterar uma tarefa    
async def change_task(task_id: int, description: str, active: bool, user_id: int):
    try:
        task_obj = select(database.dbtasks).where(database.dbtasks.id == task_id, database.dbtasks.user_id == user_id)
        async with database.async_session() as session:
            async with session.begin():
                result = await session.execute(task_obj)
                data = result.scalar_one_or_none()
                if data:
                    data.description = description
                    data.active = active
                    data.updated_at = datetime.now()
                else:
                    print(f"Tarefa não com ID {task_id} encontrada")
                    return False
                return data.to_dict()
    except SQLAlchemyError as e:
        print(f"Erro ao alterar uma tarefa no banco de dados: {e}")
        return False
