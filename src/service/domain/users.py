import copy
import uuid
from src.utils.mongodb.mongodb import MongoService
from bson.objectid import ObjectId
from src.utils.constants import USER_DB
from fastapi import HTTPException
from src.utils.logging import logger


def get_user(**kwargs):
    """
    Retrieve user information from the database.

    Args:
        kwargs: User information.


    Returns:
        dict: User information.
    """
    return MongoService.fetch(USER_DB, kwargs)


def create_user(**kwargs):
    """
    Create a new user and insert their information into the database.

    Args:
        **kwargs: User information.

    Returns:
        dict: Result of the insertion operation.
    """
    user = get_user(email=kwargs["email"])
    if user:
        raise HTTPException(
            status_code=400, detail=f"User with this email already exists with email: {kwargs['email']}")
    
    kwargs["user_id"] = str(uuid.uuid4())
    inserted_id = MongoService.insert(USER_DB, data=copy.deepcopy(kwargs))
    return kwargs


def update_user(**kwargs):
    """
    Update user information in the database.

    Args:
        **kwargs: Updated user information.

    Returns:
        dict: Result of the update operation.
    """
    user_id = kwargs.pop("user_id")
    user = get_user(user_id)
    if not user:
        return {"success": False, "error": "User not found"}

    result = MongoService.update(
        USER_DB, {"user_id": user_id}, {"$set": kwargs})
    return True



