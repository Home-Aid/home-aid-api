import copy
import uuid
from src.utils.mongodb.mongodb import MongoService
from bson.objectid import ObjectId
from src.utils.constants import EMPLOYEE_DB
from fastapi import HTTPException
from src.utils.logging import logger


def getEmployee(**kwargs):
    """
    Retrieve user information from the database.

    Args:
        kwargs: User information.


    Returns:
        dict: User information.
    """
    return MongoService.fetch(EMPLOYEE_DB, kwargs)


def createEmployee(**kwargs):
    """
    Create a new user and insert their information into the database.

    Args:
        **kwargs: User information.

    Returns:
        dict: Result of the insertion operation.
    """
    employee = getEmployee(email=kwargs["email"])
    if employee:
        raise HTTPException(
            status_code=400, detail=f"Employee with this email already exists with email: {kwargs['email']}")
    
    kwargs["employeeId"] = str(uuid.uuid4())
    inserted_id = MongoService.insert(EMPLOYEE_DB, data=copy.deepcopy(kwargs))
    return kwargs


def updateEmployee(**kwargs):
    """
    Update user information in the database.

    Args:
        **kwargs: Updated user information.

    Returns:
        dict: Result of the update operation.
    """
    employeeId = kwargs.pop("employeeId")
    employee = getEmployee(employeeId=employeeId)
    if not employee:
        return {"success": False, "error": "Employee not found"}

    result = MongoService.update(
        EMPLOYEE_DB, {"employeeId": employeeId}, {"$set": kwargs})
    return True



