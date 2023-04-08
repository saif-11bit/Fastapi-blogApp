from fastapi import APIRouter

from .endpoints.post import router as post_router
from .endpoints.user import router as user_router
from .endpoints.auth import router as auth_router
from .endpoints.comment import router as comment_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(post_router)
router.include_router(user_router)
router.include_router(comment_router)
