from functools import lru_cache

from fastapi import Depends

from src.repos.employee import EmployeeRepository
from src.services.employee import EmployeeService


@lru_cache
def get_employee_repo():
    return EmployeeRepository(

    )


@lru_cache
def get_employee_service(repo=Depends(get_employee_repo)):
    return EmployeeService(
        repo=repo
    )
