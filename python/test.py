from fastapi import FastAPI, Depends, HTTPException
from auth import AuthChecker
from schema import AuthDetails

app = FastAPI()

auth_handler = AuthChecker()
users = []


@app.post('/register')
def register(auth_details: AuthDetails):
    if any(x['first_name'] == auth_details.first_name and
           x['last_name'] == auth_details.last_name and
           x['email'] == auth_details.email
           for x in users):
        raise HTTPException(status_code=400, detail='Username already exists')
    hash_passwd = auth_handler.get_password_hash(auth_details.password)
    users.append({'first_name': auth_details.first_name, 
                  'last_name': auth_details.last_name, 
                  'email': auth_details.email, 
                  'password': hash_passwd})
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    user = None 
    for x in users:
        if (x['first_name'] == auth_details.first_name or
            x['last_name'] == auth_details.last_name or
            x['email'] == auth_details.email):
            user = x
            break

    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    token = auth_handler.encode_token(user['first_name'], user['last_name'], user['email'])
    return {'token': token}


@app.get('/unprotected')
def unprotected():  
    return {'message': 'hello world'}


@app.get('/protected')
def protected(user_data=Depends(auth_handler.auth_wrapper) ):
    first_name = user_data[0]
    last_name = user_data[1]
    return {
        'name': first_name,
        'last_name': last_name
    }