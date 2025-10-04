from pydantic import BaseModel


class EmployeeIn(BaseModel):
    first_name: str
    last_name: str
    age: int


class Employee(BaseModel):
    id: str
    first_name: str
    last_name: str
    age: int


class EmployeeOut(BaseModel):
    id: str
    first_name: str
    last_name: str
    age: int


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    age: int | None = None
