from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from . import database
    
# Função para obter a tarefa pelo ID
async def get_user_by_id(user_id: int):
    try:
        stmt = select(database.dbusers).where(database.dbusers.id == user_id)
        async with database.async_session() as session:
            result = await session.execute(stmt)
            data = result.scalar_one_or_none()
            return data.to_dict() if data else None
    except SQLAlchemyError as e:
        print(f"Erro ao obter a tarefa pelo id: {e}")
        return False    

# Função para adicionar uma novo usuário
async def add_user(username: str, password: str):
    try:
        new_user = database.dbusers(username = username, password = pbkdf2_sha256.hash(password))
        async with database.async_session() as session:                                                                                                     
            async with session.begin():
                session.add(new_user)
            await session.refresh(new_user)
            return new_user.to_dict()
    except IntegrityError:
        print(f"Usuário já existente")
        return -1
    except SQLAlchemyError as e:
        print(f"Erro ao adicionar uma novo usuario no banco de dados: {e}")
        return False

# Função para alterar os dados do usuário
async def change_user(id: int, username: str, password: str):
    try:
        stmt = select(database.dbusers).where(database.dbusers.id == id)
        async with database.async_session() as session:
            async with session.begin():
                result = await session.execute(stmt)
                user = result.scalar_one_or_none()
                if user:
                    user.username = username
                    user.password = pbkdf2_sha256.hash(password)
                    user.updated_at = datetime.now()
                else:
                    print(f"Usuario {username} nao encontrado: {id}")
                    return None
                return user.to_dict()
    except IntegrityError as e:
        print(f"Tentando alterar o usuario para um username existente: {username}")
        return -1
    except SQLAlchemyError as e:
        print(f"Erro ao consultar o usuario para alteracao: {e}")
        return False
                
    

# Função para verificar se o usuário/senha é válido
async def check_user(username: str, password: str):
    try:
        stmt = select(database.dbusers).where(database.dbusers.username == username)
        async with database.async_session() as session:
            result = await session.execute(stmt)
            data = result.scalar_one_or_none()
        if data is None:
            return False
        else:
            if pbkdf2_sha256.verify(password, data.password):
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(f"Erro ao validar usuario/senha no banco de dados: {e}")
        return False
    
# Funçao para retornar o user id
async def get_user_id(username: str):
    try:
        stmt = select(database.dbusers).where(database.dbusers.username == username)
        async with database.async_session() as session:
            result = await session.execute(stmt)
            data = result.scalar_one_or_none()

        if data is None:
            return False
        else:
            return data.id
    except SQLAlchemyError as e:
        print(f"Erro ao consultar o user id: {e}")
        return False
    