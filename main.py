from fastapi import FastAPI
from fastapi import Depends

from fastapi import status
from fastapi.exceptions import HTTPException

from fastapi.security import OAuth2PasswordRequestForm

from model import User

app = FastAPI()

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    if User.login(form_data.username, form_data.password):

        return {
            'mensaje': 'Usuario Autenticado'
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