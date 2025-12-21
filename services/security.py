import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Carrega variaveis de ambiente
load_dotenv()
secret_key = os.getenv("secret_key")

# Define os parametros para o token
hash_algorithm = "RS256"
token_expires_minutes = 15

# Cria o token
def token(username = str, password = str):
    encoded_data = {
        "username": username,
        "password": password,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=token_expires_minutes)
    }
    generated_token = jwt.encode(encoded_data, secret_key, algorithm=hash_algorithm)
    return(generated_token)
