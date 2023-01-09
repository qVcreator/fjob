from fastapi import Depends
from sqlalchemy.orm import Session

from .. import models, tables
from ..database import get_session


class SuggestionsService:
    def __init__(self,
                 session: Session = Depends(get_session)):
        self.session = session

    def create_comment(
            self,
            user_to_id: int,
            comment_data: models.CreateComment):

        comment = tables.Comments(**comment_data.dict())
        comment.is_deleted = False

        self.session.add(comment)
        self.session.commit()

    def delete_commit(
            self,
            comment_id: int
    ):
        comment = (
            self.session
            .query(tables.Comments)
            .filter_by(id=comment_id)
            .first()
        )

        comment.is_deleted = True

        self.session.commit()
