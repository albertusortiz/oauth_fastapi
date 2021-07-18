import jwt

from datetime import datetime
from datetime import timedelta

from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from fastapi import status

from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

from model import User

app = FastAPI()

SECRET = "codigofacilito"

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_token(username):
    data = {
        "usernamne": username,
        "exp": datetime.utcnow() + timedelta(days=5)
    }
    # Guardemos el access token en la BD
    # Generemos un refresh token
    return jwt.encode(data, SECRET, algorithm="HS256")


def decode_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        return None


def get_current_user(token: str = Depends(oauth2_schema)):
    data = decode_token(token)

    if data and data.get('username') and data.get('exp'):
        
        if datetime.fromtimestamp(data['exp']) > datetime.utcnow():
            return data.get('username')

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="El token no es valido.",
        headers={"WWW-Authenticate": "Bearer"}
    )


@app.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    if User.login(form_data.username, form_data.password):

        return {
            'access_token': create_token(form_data.username),
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
async def me(user: str = Depends(get_current_user)):
    print(user)
    return {
        "mensaje": "Hola Mundo"
    }