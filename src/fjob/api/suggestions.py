from fastapi import APIRouter, Depends, status

from .. import models
from ..services import role
from ..services.suggestions import SuggestionsService

router = APIRouter(
    prefix="/suggestions",
    tags=['suggestions']
)


@router.post('/{suggestion_id}')
def suggestion_reply():
    return []


@router.post(
    '/',
    response_model=int,
    status_code=status.HTTP_201_CREATED
)
def create_suggestion(suggestion_data: models.SuggestionCreate,
                      current_user: models.AuthUser = Depends(role.RoleChecker([
                          models.Role.USER
                      ])),
                      suggestions_service: SuggestionsService = Depends()
                      ):
    suggestions_service.create_suggestion(suggestion_data)


@router.put('/{suggestion_id}')
def update_suggestion():
    return []


@router.patch('/{suggestion_id}')
def update_suggestion_status():
    return []


@router.delete('/suggestion_delete')
def delete_suggestion():
    return []
