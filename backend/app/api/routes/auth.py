from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.user_service import (
    register_user,
    authenticate_user
)

from app.core.security import (
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


class AuthRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(
    data: AuthRequest
):
    result = register_user(
        data.email,
        data.password
    )

    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("message"))

    return result


@router.post("/login")
async def login(
    data: AuthRequest
):
    user = authenticate_user(
        data.email,
        data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user["email"]
    })

    return {
        "success": True,
        "access_token": token,
        "token_type": "bearer"
    }
