import jwt

from datetime import datetime
from datetime import timedelta

from fastapi import FastAPI
from fastapi import Depends

from fastapi import status
from fastapi.exceptions import HTTPException

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from model import User

app = FastAPI()

SECRET = "codigofacilito"

def create_token(username):
    data = {
        "usernamne": username,
        "exp": datetime.now() + timedelta(days=7)
    }

    return jwt.encode(data, SECRET, algorithm="HS256")

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    if User.login(form_data.username, form_data.password):

        return {
            'token': create_token(form_data.username),
            'token_type': 'bearer'
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return {
        'mensaje': 'login'
    }

@app.get('/me')
async def me():
    return {
        "mensaje": "Hola Mundo"
    }