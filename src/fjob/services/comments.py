from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, tables
from ..database import get_session


class CommentsService:
    def __init__(self,
                 session: Session = Depends(get_session)):
        self.session = session

    def create_comment(
            self,
            comment_data: models.CreateComment,
            current_user_role: models.Role
):
        user_to = (
            self.session
            .query(tables.BaseUser)
            .filter_by(id=comment_data.user_to_id)
            .first()
        )

        if user_to.role == current_user_role:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        comment = tables.Comments(**comment_data.dict())
        comment.is_deleted = False

        self.session.add(comment)
        self.session.commit()

    def delete_comment(
            self,
            comment_id: int,
            current_user_id: int
    ):
        comment = (
            self.session
            .query(tables.Comments)
            .filter_by(id=comment_id)
            .first()
        )

        if current_user_id != comment.user_from_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        comment.is_deleted = True

        self.session.commit()
