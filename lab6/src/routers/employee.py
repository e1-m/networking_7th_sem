from typing import Annotated

from fastapi import APIRouter, status, Depends

from src.deps import get_employee_service
from src.models.employee import EmployeeOut, EmployeeIn, EmployeeUpdate
from src.services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("/", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeIn,
                    service: Annotated[EmployeeService, Depends(get_employee_service)]):
    return service.create(data)


@router.get("/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: str,
                 service: Annotated[EmployeeService, Depends(get_employee_service)]):
    return service.get(emp_id)


@router.get("/", response_model=list[EmployeeOut])
def list_employees(service: Annotated[EmployeeService, Depends(get_employee_service)]):
    return service.list()


@router.put("/{emp_id}", response_model=EmployeeOut)
def update_employee(emp_id: str,
                    data: EmployeeIn,
                    service: Annotated[EmployeeService, Depends(get_employee_service)]):
    return service.update(emp_id, data)


@router.patch("/{emp_id}", response_model=EmployeeOut)
def patch_employee(emp_id: str,
                   data: EmployeeUpdate,
                   service: Annotated[EmployeeService, Depends(get_employee_service)]):
    return service.patch(emp_id, data)


@router.delete("/{emp_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(emp_id: str,
                    service: Annotated[EmployeeService, Depends(get_employee_service)]):
    service.delete(emp_id)
