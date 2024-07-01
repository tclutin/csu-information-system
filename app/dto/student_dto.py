from pydantic import BaseModel


class CreateStudentDTO(BaseModel):
    specialty_name: str
