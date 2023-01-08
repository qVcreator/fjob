from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from fjob.database import get_session
from .. import models, tables


class SuggestionsService:
    def __init__(self,
                 session: Session = Depends(get_session)):
        self.session = session

    def create_suggestion(self,
                          suggestion_data: models.SuggestionCreate) -> int:
        suggestion = tables.Suggestions(**suggestion_data.dict())
        suggestion.status = models.Status.CREATED

        self.session.add(suggestion)
        self.session.commit()

        return suggestion.id

    def update_suggestion(self,
                          suggestion_id: int,
                          current_user_id: int,
                          suggestion_data: models.SuggestionUpdate):
        suggestion = (
            self.session
            .query(tables.Suggestions)
            .filter_by(id=suggestion_id)
            .first()
        )

        if suggestion.user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        for field, value in suggestion_data:
            setattr(suggestion, field, value)

        self.session.commit()

    def suggestion_reply(self,
                         executor_id: int,
                         suggestion_id: int):
        suggestion = (
            self.session
            .query(tables.Suggestions)
            .filter_by(id=suggestion_id)
            .first()
        )

        if suggestion.status != models.Status.CREATED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

        suggestion.executor_id = executor_id
        suggestion.status = models.Status.IN_PROGRESS

        self.session.commit()