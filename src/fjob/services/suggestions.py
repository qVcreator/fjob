from fastapi import Depends
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

    def