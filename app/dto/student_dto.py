import base64
from io import BytesIO
from typing import Annotated

from PIL import Image
from annotated_types import MinLen, MaxLen
from fastapi import UploadFile
from pydantic import BaseModel


class CreateStudentDTO(BaseModel):
    fullname: Annotated[str, MinLen(5), MaxLen(50)]
    group_id: int
    tgchat_id: int
    student_card: bytes

    @classmethod
    async def from_form(cls, fullname: str, group_id: int, tgchat_id: int, student_card: UploadFile):
        if not student_card.content_type.startswith('image/'):
            raise ValueError("The uploaded file is not an image.")

        if student_card.size > 5 * 1024 * 1024:
            raise ValueError("The uploaded file is too large.")

        try:
            image_data = await student_card.read()
            image = Image.open(BytesIO(image_data))
            image.verify()
        except Exception:
            raise ValueError("The uploaded file is not a valid image.")

        return cls(
            fullname=fullname,
            group_id=group_id,
            tgchat_id=tgchat_id,
            student_card=image_data
        )