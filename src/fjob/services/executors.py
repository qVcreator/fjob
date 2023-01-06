from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import AuthService
from .. import tables, models
from ..database import get_session


class ExecutorsService:
    def __init__(self,
                 session: Session = Depends(get_session),
                 auth_service: AuthService = Depends()):
        self.session = session
        self.auth_service = auth_service

    def get_executor_by_id(self, executor_id: int) -> tables.Executors:
        executor = (
            self.session
            .query(tables.Executors)
            .filter_by(id=executor_id)
            .first()
        )

        if not executor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return executor

    def create_executor(self,
                        executor_data: models.CreateUser) -> models.Token:
        executor = tables.BaseUser(
            email=executor_data.email,
            first_name=executor_data.first_name,
            second_name=executor_data.second_name,
            date_create=datetime.now(),
            role=models.Role.EXECUTOR,
            is_deleted=False,
            password=self.auth_service.hash_password(executor_data.password),
        )
        self.session.add(executor)
        self.session.commit()
        return self.auth_service.create_token(executor)

    def update_executor_information(self,
                                    executor_data: models.UpdateExecutor,
                                    executor_id: int,):
        executor = (
            self.session
            .query(tables.Executors)
            .filter_by(id=executor_id)
            .first()
        )

        if not executor:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User does not exist')

        for field, value in executor_data:
            setattr(executor, field, value)

        self.session.commit()
