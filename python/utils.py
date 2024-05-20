def register_form_validator(name : str, surname : str, email: str, password : str, phone : str):
    if name.isalpha() and surname.isalpha() and '@' in email and email.split('@')[1] != '' and len(password) >= 4 and len(phone) == 9:
        return True
    else:
        return False
    
    
def login_form_validar(email: str,  password: str):
    if '@' in email and email.split('@')[1] != '' and len(password) >= 4:   
        return True
    else:
        return False
    
from singleton import DataBase
def check_if_account_exists(password_hash, email):
    db = DataBase()
    results = db.data_valid_login(password_hash, email)
    if results:
        return True
    else:
        return False
    