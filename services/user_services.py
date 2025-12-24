import json
from sqlalchemy import insert, select, update, delete, func
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from . import database

# Função para obter a tarefa pelo USERNAME
def get_user_by_username(username: str):
    try:
        stmt = select(database.dbusers).where(database.dbusers.c.username == username)
        with database.engine.begin() as conn:
            row = conn.execute(stmt).one_or_none()
            if row is None:
                return None
        display_fields = {
            'id': row.id,
            'username': row.username
        }
        return display_fields
        #return row._asdict()
    except SQLAlchemyError as e:
        print(f"Erro ao obter a tarefa pelo id: {e}")
        return False
    
# Função para obter a tarefa pelo ID
def get_user_by_id(user_id: int):
    try:
        stmt = select(database.dbusers).where(database.dbusers.c.id == user_id)
        with database.engine.begin() as conn:
            row = conn.execute(stmt).one_or_none()
            if row is None:
                return None
        display_fields = {
            'id': row.id,
            'username': row.username,
            'created_at': row.created_at,
            'updated_at': row.updated_at
        }
        return display_fields
        #return row._asdict()
    except SQLAlchemyError as e:
        print(f"Erro ao obter a tarefa pelo id: {e}")
        return False    

# Função para adicionar uma novo usuário
def add_user(username: str, password: str):
    try:
        stmt = insert(database.dbusers).values(username=username, password=pbkdf2_sha256.hash(password)).returning(database.dbusers.c.id, 
                                                                                                            database.dbusers.c.username, 
                                                                                                            database.dbusers.c.password, 
                                                                                                            database.dbusers.c.created_at, 
                                                                                                            database.dbusers.c.updated_at)
        with database.engine.begin() as conn:
            result = conn.execute(stmt).one_or_none()
        
        if result is None:
            return None
        return result._asdict()
    except SQLAlchemyError as e:
        print(f"Erro ao adicionar uma novo usuario no banco de dados: {e}")
        return False

# Função para verificar se o usuário/senha é válido
def check_user(username: str, password: str):
    try:
        stmt = select(database.dbusers).where(database.dbusers.c.username == username)
        with database.engine.begin() as conn:
            result = conn.execute(stmt).one_or_none()
        
        if result is None:
            return False
        else:
            if pbkdf2_sha256.verify(password, result.password):
                return True
            else:
                return False
    except SQLAlchemyError as e:
        print(f"Erro ao validar usuario/senha no banco de dados: {e}")
        return False
    
# Funçao para retornar o user id
def get_user_id(username: str):
    try:
        stmt = select(database.dbusers).where(database.dbusers.c.username == username)
        with database.engine.begin() as conn:
            result = conn.execute(stmt).one_or_none()

        if result is None:
            return False
        else:
            return result.id
    except SQLAlchemyError as e:
        print(f"Erro ao consultar o user id: {e}")
        return False
    