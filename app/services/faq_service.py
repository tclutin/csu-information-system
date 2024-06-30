from datetime import datetime
from typing import Optional, List

from dto.faq_dto import CreateFAQDTO, CreateFAQListDTO
from infrastructure.models import FAQ
from repositories import faq_repository
from repositories.faq_repository import FAQRepository


class FAQService:
    def __init__(self, faq_repository: FAQRepository):
        self.faq_repository = faq_repository

    # FAQService methods
    async def create(self, dto: CreateFAQListDTO) -> List[FAQ]:
        faqs = []
        for item in dto.faqs:
            existing_faq = await self.get_by_question(item.question)
            if existing_faq is not None:
                raise ValueError(f"Question '{item.question}' already exists")

            faq = FAQ(
                question=item.question,
                answer=item.answer,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            faqs.append(faq)

        return await self.faq_repository.create(faqs)

    async def delete(self, faq_id: int) -> None:
        faq = await self.get_by_id(faq_id)
        if faq is None:
            raise ValueError("FAQ does not exist")

        await self.faq_repository.delete(faq)

    async def get_by_question(self, question: str) -> Optional[FAQ]:
        return await self.faq_repository.get_by_question(question)

    async def get_by_id(self, faq_id: int) -> Optional[FAQ]:
        return await self.faq_repository.get_by_id(faq_id)

    async def get_all(self) -> List[FAQ]:
        return await self.faq_repository.get_all()