from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserModel, UserGroupEnum, UserGroupModel
from schemas import UserRegistrationRequestSchema
from security.passwords import hash_password


async def create_user(db: AsyncSession, user: UserRegistrationRequestSchema) -> UserModel:
    hashed = hash_password(user.password)
    group_id = await db.scalar(
        select(UserGroupModel.id)
        .where(UserGroupModel.name == UserGroupEnum.USER)
    )
    db_user = UserModel(
        email=user.email,
        _hashed_password=hashed,
        group_id=group_id
    )
    db.add(db_user)
    await db.flush()
    return db_user


async def get_user_by_email(db: AsyncSession, email: str) -> UserModel | None:
    return await db.scalar(select(UserModel).where(UserModel.email == email))
