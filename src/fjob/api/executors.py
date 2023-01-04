from fastapi import APIRouter

router = APIRouter(
    prefix="/executors",
    tags=['executors']
)


@router.put('/')
def update_executor_information():
    return []


@router.patch('/')
def update_executors_categories():
    return []
