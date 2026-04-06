from sqlmodel import SQLModel
from app.db.session import engine

# Import all models so SQLModel.metadata is populated before create_all
import app.models.todo  # noqa: F401
import app.models.todo_dependency  # noqa: F401
import app.models.todo_history  # noqa: F401


async def create_db_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
