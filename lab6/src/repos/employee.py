import uuid
from typing import Optional

from src.models.employee import Employee, EmployeeIn, EmployeeOut, EmployeeUpdate


class EmployeeRepository:
    def __init__(self):
        self._employees: dict[str, Employee] = {}

    def create(self, data: EmployeeIn) -> EmployeeOut:
        emp_id = str(uuid.uuid4())
        employee = Employee(id=emp_id, **data.model_dump())
        self._employees[emp_id] = employee
        return EmployeeOut(**employee.model_dump())

    def get(self, emp_id: str) -> Optional[EmployeeOut]:
        employee = self._employees.get(emp_id)
        return EmployeeOut(**employee.model_dump()) if employee else None

    def list(self) -> list[EmployeeOut]:
        return [EmployeeOut(**emp.model_dump()) for emp in self._employees.values()]

    def update(self, emp_id: str, data: EmployeeUpdate) -> Optional[EmployeeOut]:
        if emp_id not in self._employees:
            return None

        stored_employee = self._employees[emp_id]
        update_data = data.model_dump(exclude_none=True)

        updated_employee = stored_employee.model_copy(update=update_data)
        self._employees[emp_id] = updated_employee
        return EmployeeOut(**updated_employee.model_dump())

    def delete(self, emp_id: str) -> bool:
        return self._employees.pop(emp_id, None) is not None
