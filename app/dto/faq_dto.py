from typing import List

from pydantic import BaseModel


class CreateFAQDTO(BaseModel):
    question: str
    answer: str


class CreateFAQListDTO(BaseModel):
    faqs: List[CreateFAQDTO]
