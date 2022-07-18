""" Modules """
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from passlib.context import CryptContext
from datetime import datetime, timedelta

"""

Modules Explanation:

jwt: JSON Web Token for encoding and decoding JSON objects.

HTTPException: It will be used to raise errors for invalid tokens which the
               framework handles to return an error to user with provided
               status code and error message.

Security: It is used for dependency injection and will highlight routes that
          require authorization headers in the swagger ui and provide a way to
          enter bearer token.

HttpBearer: It is going to be used as part of dependency injection to ensure a
            valid auth header has been provided when calling the endpoint.

HttpAuthorizationCredentials: Is the object type that will be returned from
                              that dependency injection.

CryptContext: To create a context for hashing and validating passwords.

"""


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = "SECRET"

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=
                                status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='Signature has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials =
                                 Security(security)):
        return self.decode_token(auth.credentials)
