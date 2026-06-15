from dotenv import load_dotenv as load
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from pydantic import BaseModel,Field
from typing import Annotated
class user_password(BaseModel):
    p:Annotated[str,Field(min_length=6,max_length=128)]
ph=PasswordHasher()
import os 
load()
pepper=os.getenv('pepper')
def password_to_hash(password:str)->str:
    pas=f'{password}{pepper}'
    return ph.hash(pas)
def verify(hash:str,password:str):   
    pas=f'{password}{pepper}'
    try:
        ph.verify(hash,pas)
        return True
    except Exception as e:
       return False