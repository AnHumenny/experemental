from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

engine = create_async_engine(
    "sqlite+aiosqlite:///base.db"
)


new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class DBaseOrm(Model):
    __tablename__ = "main"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    full_name: Mapped[str]
    date_of_birth: Mapped[str]
    phone: Mapped[int]
    enrollment_year: Mapped[int | None]
    course: Mapped[int | None]
    major: Mapped[str | None]
    status: Mapped[str]



async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
