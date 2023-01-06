import datetime
from typing import overload, List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from fjob import tables, models
from fjob.database import get_session
from fjob.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in/')


def get_current_user(token: str = Depends(oauth2_scheme)) -> models.AuthUser:
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hash_password: str) -> bool:
        return bcrypt.verify(plain_password, hash_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def verify_token(cls, token: str) -> models.BaseUser:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=settings.JWT_ALGORITHM
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = models.BaseUser.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.BaseUser) -> models.Token:
        user_data = models.BaseUser.from_orm(user)
        now = datetime.datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=settings.JWT_EXPIRES_S),
            'sub': str(user_data.id)
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

        result = models.Token(access_token=token)
        return result

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(
            self,
            user_data: models.CreateUser,
    ) -> models.Token:
        user = tables.BasicUser(
            email=user_data.email,
            first_name=user_data.first_name,
            second_name=user_data.second_name,
            date_create=datetime.datetime.now(),
            role=models.Role.USER,
            is_deleted=False,
            password=self.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)

    def authenticate_user(
            self,
            email: str,
            password: str,
    ) -> models.Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

        user = (
            self.session
            .query(tables.BaseUser)
            .filter(tables.BaseUser.email == email)
            .first()
        )

        if not user:
            raise exception

        if not self.verify_password(password, user.password):
            raise exception

        return self.create_token(user)
