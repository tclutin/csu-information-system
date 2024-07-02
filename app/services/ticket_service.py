from datetime import datetime
from typing import List

from dto.message_dto import CreateMessageDTO
from dto.student_dto import CreateStudentDTO
from dto.ticket_dto import CreateTicketDTO
from infrastructure.models import Ticket
from repositories import student_repository
from repositories.ticket_repository import TicketRepository
from services.student_service import StudentService
from services.upload_service import UploadService


class TicketService:
    def __init__(self, ticket_repository: TicketRepository, student_service: StudentService, upload_service: UploadService):
        self.ticket_repository = ticket_repository
        self.student_service = student_service
        self.upload_service = upload_service

    async def create(self, dto: CreateTicketDTO) -> Ticket:
        if dto.type_ticket not in ["verification", "request"]:
            raise ValueError("ticket's type can be verification or request")

        if dto.type_ticket == "verification":
            if dto.fullname is None:
                raise ValueError("fullname is required for verification")

            if dto.wish_group is None:
                raise ValueError("wish_group is required for verification")

            if dto.photo is None:
                raise ValueError("phono is required for verification")

            dto.message = None

        if dto.type_ticket == "request":
            if dto.message is None:
                raise ValueError("message is required for request")

            student = await self.student_service.get_by_tgchat_id(dto.tgchat_id)
            if student is None:
                raise ValueError("tgchat_id is required for request")

            dto.fullname = student.fullname
            dto.wish_group = None

        file_name = None
        if dto.photo is not None:
            file_name = await self.upload_service.upload_file(dto.photo)

        ticket = Ticket(
            tgchat_id=dto.tgchat_id,
            fullname=dto.fullname,
            wish_group=dto.wish_group,
            type=dto.type_ticket,
            status="open",
            photo=file_name,
            message=dto.message,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.ticket_repository.create(ticket)

    async def cancel(self, ticket_id: int, dto: CreateMessageDTO) -> None:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if ticket is None:
            raise ValueError("ticket_id is invalid")

        if ticket.status == "closed":
            raise ValueError("ticket is already closed")

        #должна быть отправка сообщнеия в телеграм

        ticket.status = "closed"
        await self.ticket_repository.update(ticket)

    async def accept(self, ticket_id: int, dto: CreateMessageDTO) -> None:
        ticket = await self.ticket_repository.get_by_id(ticket_id)
        if ticket is None:
            raise ValueError("ticket_id is invalid")

        if ticket.status == "closed":
            raise ValueError("ticket is already closed")

        ticket.status = "closed"
        ticket = await self.ticket_repository.update(ticket)

        #notification сюда

        #pizdec
        group = await (
            self
            .student_service
            .group_service
            .get_by_shortname(ticket.wish_group)
        )

        if group is None:
            raise ValueError("group is invalid")

        dto = CreateStudentDTO(
            fullname=ticket.fullname,
            group_id=group.group_id,
            tgchat_id=ticket.tgchat_id,
            student_card=ticket.photo
        )

        await self.student_service.create(dto)

    async def get_all(self) -> List[Ticket]:
        return await self.ticket_repository.get_all()
