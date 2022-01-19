import time
from typing import Dict
from jose import jwt
from datetime import datetime, timedelta, timezone

JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
JWT_ALGORITHM = "HS256"
JWT_TOKEN_EXPIRE_SECONDS = 60*60*24*30*12 # 1 YEAR
PREFIX = 'Bearer '

def signJWT(userEmail: str) -> Dict[str, str]:
    payload = {
        "userEmail": userEmail,
        "expires": time.time() + JWT_TOKEN_EXPIRE_SECONDS
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def getToken(token):
    if not token.startswith(PREFIX):
        raise ValueError('Invalid token')

    return token[len(PREFIX):]

def encryptTokenPassword(email):
    payload = {
        "exp": datetime.now() + timedelta(days=1), 
        "email": email
        }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token
