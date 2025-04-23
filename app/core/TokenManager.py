from jose import jwt
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional
from services.auth import SECRET_KEY, ALGORITHM

def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
def create_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        expire = datetime.utcnow() + (expires_delta or self.access_expire)
        to_encode = {"exp": expire, **data}
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)