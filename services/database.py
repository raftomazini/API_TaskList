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

tasks = Table("tasks", metadata, autoload_with=engine)

# Função para inserir um novo registro
def tasks_insert(description):
    try:
        stmt = insert(tasks).values(description=description, active=True)
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
        # chamar a função para retornar todas as tarefas e retornar o conteúdo
        return result
    except Exception as e:
        return False

# Função para recuperar os registros
def get_tasks(status = None):
    if status == None:
        stmt = select(tasks)
    elif status:
        stmt = select(tasks).where(tasks.c.active == True)
    else:
        stmt = select(tasks).where(tasks.c.active == False)
#    stmt = select(tasks)
    try:
        tasklist = []
        with engine.connect() as conn:
            result = conn.execute(stmt)
            for row in result:
                task = {
                    'id': row.id,
                    'description': row.description,
                    'active': row.active
                }
                tasklist.append(task)
        
        return tasklist
    except Exception as e:
        return f"{e}"
    
# Inicia a conexão com o banco de dados
#def db_connect(driver, dbuser, dbpass, dbhost, dbport, dbname):
#    engine = create_engine(f"{driver}://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}")
#    return engine
    