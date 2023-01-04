from fastapi import APIRouter
from .suggestions import router as suggestions_router
from .auth import router as auth_router

router = APIRouter()
router.include_router(suggestions_router)
router.include_router(auth_router)
