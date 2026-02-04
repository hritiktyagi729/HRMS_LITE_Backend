from pydantic import BaseModel, EmailStr, validator


# schema for employee data
class EmployeeSchema(BaseModel):
    name: str
    email: EmailStr
    department: str

    class Config:
        orm_mode = True
    @validator('name')
    def name(cls, v):
        if not v:
            raise ValueError('Name must not be empty')
        if len(v) < 2 or len(v) > 100:
            raise ValueError('Name must be between 2 and 100 characters')
        return v
    @validator('department')
    def department(cls, v):
        if not v:
            raise ValueError('Department must not be empty')
        if len(v) < 2 or len(v) > 50:
            raise ValueError('Department must be between 2 and 50 characters')
        return v