from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from infrastructure.models import Group


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, group: Group) -> Group:
        self.session.add(group)
        await self.session.commit()
        return group

    async def get_all(self) -> List[Group]:
        statement = select(Group)
        result = await self.session.execute(statement)
        groups = result.scalars().all()
        return list(groups)

    async def get_by_shortname(self, shortname: str) -> Optional[Group]:
        statement = select(Group).where(Group.short_name == shortname)
        result = await self.session.execute(statement)
        return result.scalar()