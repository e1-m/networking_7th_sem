class EmployeeServiceError(Exception):
    def __init__(self, message: str = "Service is not available", headers=None):
        self.message = message
        self.headers = headers
        super().__init__(self.message)


class EmployeeNotFoundError(EmployeeServiceError):
    def __init__(self, emp_id: str):
        super().__init__(f"Employee with id '{emp_id}' not found")
        self.emp_id = emp_id


class EmployeeAlreadyExistsError(EmployeeServiceError):
    def __init__(self, emp_id: str):
        super().__init__(f"Employee with id '{emp_id}' already exists")
        self.emp_id = emp_id
