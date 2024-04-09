from pydantic import BaseModel

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    name: str
    age: int
    address: Address

class UpdateAddress(BaseModel):
    city: str=None
    country: str=None

class UpdateStudent(BaseModel):
    name: str = None
    age: int = None
    address: UpdateAddress =None
