import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import serialization
from . import user_services

# Carrega variaveis de ambiente
load_dotenv()
#secret_key = os.getenv("secret_key")
private_key = os.getenv("private_key")
public_key = os.getenv("public_key")

# Define os parametros para o token
hash_algorithm = "RS256"
#hash_algorithm = "HS256"
token_expires_minutes = 15

# Cria o token
def token(username = str, password = str):
    valid_user = user_services.check_user(username=username, password=password)
    if valid_user:
        user_id = user_services.get_user_id(username)
        if user_id:
            encoded_data = {
                "id": user_id,
                "username": username,
                "exp": datetime.now(timezone.utc) + timedelta(minutes=token_expires_minutes)
            }
            generated_token = jwt.encode(encoded_data, private_key, algorithm=hash_algorithm)
            #generated_token = jwt.encode(encoded_data, secret_key, algorithm=hash_algorithm)
            result = {
                "token": generated_token
            }
            return(result)
        else:
            return False
    else:
        return False

def check_token(token: str):
    try:
        decoded_token = jwt.decode(token, public_key, algorithms=[hash_algorithm])
        result = {
            "id": decoded_token['id'],
            "username": decoded_token['username']
        }
        return result
    except jwt.ExpiredSignatureError:
        print("Token expirado")
        return -1
    except jwt.InvalidTokenError:
        print("Token invalido")
        return False
    

