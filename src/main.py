from fastapi import FastAPI, Depends, HTTPException, status
from .auth import AuthHandler
from .schemas import AuthDetails

app = FastAPI()

# Its an authentication object
auth_handler = AuthHandler()

# To hold users username and password like a database it can replaced with
# SQL or NOSql database

users_list = []


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users_list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Username is taken')

    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users_list.append({
        'username': auth_details.username,
        'password': hashed_password
        })

    return {}


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for user_x in users_list:
        if user_x['username'] == auth_details.username:
            user = user_x
            break

    if (user is None) or (not auth_handler.verify_password(
                            auth_details.password, user['password'])):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid Username and/or Password')

    token = auth_handler.encode_token(user['username'])
    return {'token': token}


@app.get('/unprotected')
def unprotected():
    return {'hello': 'world'}


@app.get('/protected')                         
def protected(username=Depends(auth_handler.auth_wrapper)):
    return {'name': username}
