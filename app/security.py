from pwdlib import PasswordHash
import jwt
from dotenv import load_dotenv
import os
load_dotenv()

pwd_hash=PasswordHash.recommended()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def hash_pwd(password):
    hashed_pwd=pwd_hash.hash(password)
    return hashed_pwd
def verify(password,hashed_pwd):
    return pwd_hash.verify(password,hashed_pwd)
def create_access_token(id,role):
    payload={
        "user_id":id,
        "role":role
    }
    token=jwt.encode(
    payload,
    SECRET_KEY,
    algorithm=ALGORITHM
   
)
    return token

    
    

