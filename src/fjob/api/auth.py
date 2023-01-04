from fastapi import APIRouter

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/sign-up/')
def sign_up():
    return []


@router.post('/sign-in/')
def sign_in():
    return []
