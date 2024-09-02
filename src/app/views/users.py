from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional
# from src.lib.validator import users as users_validator
# from src.lib.domain import users as users_domain
from src.app.validator import users as users_validator
from src.service.domain import users as users_domain
router = APIRouter()


@router.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: str, request: Request):
    result = users_domain.get_user(user_id=user_id)
    if not result:
        return JSONResponse(content={"error": "User not found"}, status_code=404)
    return result


@router.post("/users", tags=["Users"])
def create_user(msg: users_validator.CreateUser, request: Request):
    result = users_domain.create_user(**msg.dict())
    return result


@router.put("/users/{user_id}", tags=["Users"])
def update_user(user_id: str, msg: users_validator.CreateUser, request: Request):
    result = users_domain.update_user(user_id=user_id, **msg.dict())
    return result
