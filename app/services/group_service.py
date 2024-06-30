from datetime import datetime
from typing import Optional

from dto.group_dto import CreateGroupDTO
from infrastructure.models import Group
from repositories.group_repository import GroupRepository


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    # DepartmentService methods
    async def create(self, dto: CreateGroupDTO) -> Group:
        group = await self.get_by_shortname(dto.shortname)
        if group is not None:
            raise ValueError('Group already exists')

        group = Group(
            short_name=dto.shortname,
            specialty=dto.specialty,
            department=dto.department,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return await self.group_repository.create(group)

    async def get_by_shortname(self, shortname: str) -> Optional[Group]:
        return await self.group_repository.get_by_shortname(shortname)

    async def get_all(self) -> list[Group]:
        return await self.group_repository.get_all()

