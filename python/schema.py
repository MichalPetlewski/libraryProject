from pydantic import BaseModel

class AuthDetails(BaseModel):
    first_name : str
    last_name : str
    email : str
    password : str
    