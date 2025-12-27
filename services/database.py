from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncAttrs, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, class_mapper
from sqlalchemy import BigInteger, String, DateTime, Integer, Boolean, ForeignKey, func
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
engine = create_async_engine(f"{driver}://{dbuser}:{dbpass}@{dbhost}:{dbport}/{dbname}", echo=False)

# Cria uma fábrica de sessões assíncronas
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Cria a classe base
class Base(AsyncAttrs, DeclarativeBase):
    # Retorna os dados como dicionário
    def to_dict(self):
        return {column.key: getattr(self, column.key) for column in class_mapper(self.__class__).columns}

# Definição da tabela users
class dbusers(Base):
    __tablename__   = "users"
    id              = mapped_column(Integer, primary_key=True, autoincrement=True)
    username        = mapped_column(String(100), nullable=False, unique=True)
    password        = mapped_column(String(255), nullable=False)
    created_at      = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at      = mapped_column(DateTime(timezone=True), onupdate=func.now())

# Definição da tabela tasks
class dbtasks(Base):
    __tablename__   = "tasks"
    id              = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    description     = mapped_column(String(500), nullable=False)
    active          = mapped_column(Boolean, nullable=False, default=True)
    user_id         = mapped_column(Integer, ForeignKey("users.id"))
    created_at      = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at      = mapped_column(DateTime(timezone=True), onupdate=func.now())
