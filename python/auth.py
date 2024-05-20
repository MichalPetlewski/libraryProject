import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime,  timedelta


class AuthChecker():
    security = HTTPBearer()
    passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = 'SECRET'
    
    def get_password_hash(self, password):
        return self.passwd_context.hash(password)
    
    def verify_password(self, plain_passwd, passwd_hash):
        return self.passwd_context.verify(plain_passwd, passwd_hash)
    
    def encode_token(self, uEmail):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': uEmail
        }
    
        token = jwt.encode(payload, self.secret, algorithm='HS256')
        return token
        
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)