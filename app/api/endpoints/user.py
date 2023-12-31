from fastapi import APIRouter, HTTPException, Depends

from app.core.user import fastapi_users, auth_backend_user, current_superuser
from app.schemas.user import UserRead, UserCreate, UserUpdate


router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend_user),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(current_superuser)],
)
# router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )
# router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
    include_in_schema=False,
)


@router.delete(
    "/users/{id}", tags=["users"], deprecated=True, include_in_schema=False
)
def delete_user(id: str):
    raise HTTPException(
        status_code=405, detail="Удаление пользователей запрещено!"
    )
