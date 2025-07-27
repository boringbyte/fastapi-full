from .models import UserTable
from .schemas import UserCreateModel
from .utils import generate_passwd_hash
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select


class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession):
        stmt = select(UserTable).where(UserTable.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        return user

    async def user_exists(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        return True if user else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = UserTable(**user_data_dict)
        new_user.password_hash = generate_passwd_hash(user_data_dict["password"])
        session.add(new_user)
        await session.commit()
        return new_user
        
