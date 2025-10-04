from src.errors import EmployeeAlreadyExistsError, EmployeeNotFoundError
from src.models.employee import EmployeeIn, EmployeeOut, EmployeeUpdate
from src.repos.employee import EmployeeRepository


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self._repo = repo

    def create(self, data: EmployeeIn) -> EmployeeOut:
        return self._repo.create(data)

    def get(self, emp_id: str) -> EmployeeOut:
        if emp := self._repo.get(emp_id) is None:
            raise EmployeeNotFoundError(emp_id)
        return emp

    def list(self) -> list[EmployeeOut]:
        return self._repo.list()

    def update(self, emp_id: str, data: EmployeeIn) -> EmployeeOut:
        if not self._repo.get(emp_id):
            raise EmployeeNotFoundError(emp_id)

        self._repo.update(emp_id, EmployeeUpdate(**data.model_dump()))
        return self._repo.get(emp_id)

    def patch(self, emp_id: str, data: EmployeeUpdate) -> EmployeeOut:
        if not self._repo.get(emp_id):
            raise EmployeeNotFoundError(emp_id)

        updated = self._repo.update(emp_id, data)
        return updated

    def delete(self, emp_id: str):
        if not self._repo.delete(emp_id):
            raise EmployeeNotFoundError(emp_id)
