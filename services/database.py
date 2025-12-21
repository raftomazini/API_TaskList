from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete
from dotenv import load_dotenv
import os

# Carrega variaveis de ambiente
load_dotenv()
driver = os.getenv("driver")
dbuser = os.getenv("dbuser")
dbpass = os.getenv("dbpass")
dbhost = os.getenv("dbhost")
dbport = os.getenv("dbport")
dbname = os.getenv("dbname")

# Cria a conexão com o banco de dados
engine = create_engine(f"{driver}://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}")

# Cria o objeto de metadados
metadata = MetaData()

# Importa a tabela do banco de dados para o objeto
dbtasks = Table("tasks", metadata, autoload_with=engine)
dbusers = Table("users", metadata, autoload_with=engine)

    