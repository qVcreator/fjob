from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import AuthService
from .. import tables, models
from ..database import get_session


class UsersService:
    def __init__(self,
                 session: Session = Depends(get_session),
                 auth_service: AuthService = Depends()):
        self.session = session
        self.auth_service = auth_service

    def get_user_by_id(self, user_id: int) -> tables.BasicUser:
        user = (
            self.session
            .query(tables.BasicUser)
            .filter_by(id=user_id)
            .first()
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user

    def create_user(self,
                    user_data: models.CreateUser) -> models.Token:
        user_check = (
            self.session
            .query(tables.BasicUser)
            .filter_by(email=user_data.email)
            .first()
        )

        if user_check:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with this email already exist')

        user = tables.BasicUser(
            email=user_data.email,
            first_name=user_data.first_name,
            second_name=user_data.second_name,
            date_create=datetime.now(),
            role=models.Role.USER,
            is_deleted=False,
            password=self.auth_service.hash_password(user_data.password),
        )
        self.session.add(user)
        self.session.commit()
        return self.auth_service.create_token(user)

    def update_user_information(self,
                                user_data: models.UpdateUser,
                                user_id: int):
        user = (
            self.session
            .query(tables.BasicUser)
            .filter_by(id=user_id)
            .first()
        )

        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user does not exist")

        for field, value in user_data:
            setattr(user, field, value)

        self.session.commit()
