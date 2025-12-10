from sqlalchemy import MetaData, Table, insert, select, update, delete
from dotenv import load_dotenv
import os
import database

# Carrega variaveis de ambiente
load_dotenv()
driver = os.getenv("driver")
dbuser = os.getenv("dbuser")
dbpass = os.getenv("dbpass")
dbhost = os.getenv("dbhost")
dbport = os.getenv("dbport")
dbname = os.getenv("dbname")

# Cria a conexão com o banco de dados
engine = database.db_connect(driver, dbuser, dbpass, dbhost, dbport, dbname)

# Cria o objeto de metadados
metadata = MetaData()

tasks = Table("tasks", metadata, autoload_with=engine)


