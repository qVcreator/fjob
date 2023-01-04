from fastapi import APIRouter

router = APIRouter(
    prefix="/suggestions",
    tags=['suggestions']
)


@router.post('/{suggestion_id}')
def suggestion_reply():
    return []


@router.post('/', response_model=int)
def create_suggestion():
    return 1


@router.put('/{suggestion_id}')
def update_suggestion():
    return []


@router.patch('/{suggestion_id}')
def update_suggestion_status():
    return []


@router.delete('/suggestion_delete')
def delete_suggestion():
    return []
