from fastapi import FastAPI
from fastapi import Depends

from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()

@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username)
    print(form_data.password)
    
    return {
        'mensaje': 'login'
    }

@app.get('/me')
async def me():
    return {
        "mensaje": "Hola Mundo"
    }