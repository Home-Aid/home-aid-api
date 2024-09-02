from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional
# from src.lib.validator import users as users_validator
# from src.lib.domain import users as users_domain
from src.app.validator import employee as employeeValidator
from src.service.domain import employee as employeeDomain
router = APIRouter()


@router.get("/employee/{employeeId}", tags=["Employee"])
def get_employee(employeeId: str, request: Request):
    result = employeeDomain.getEmployee(employeeId=employeeId)
    if not result:
        return JSONResponse(content={"error": "Employee not found"}, status_code=404)
    return result


@router.post("/employee", tags=["Employee"])
def create_employee(msg: employeeValidator.CreateEmployee, request: Request):
    result = employeeDomain.createEmployee(**msg.dict())
    return result


@router.put("/employee/{employeeId}", tags=["Employee"])
def update_employee(employeeId: str, msg: employeeValidator.CreateEmployee, request: Request):
    result = employeeDomain.updateEmployee(employeeId=employeeId, **msg.dict())
    return result
