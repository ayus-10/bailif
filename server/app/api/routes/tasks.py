import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.task import Task

router = APIRouter()


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    assignee: str = ""
    tags: str = ""


class TaskOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    assignee: str
    status: str
    tags: str

    class Config:
        from_attributes = True


@router.get("", response_model=list[TaskOut])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task))
    return result.scalars().all()


@router.post("", response_model=TaskOut)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = Task(**payload.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    # TODO: after commit, generate an embedding for title+description
    # and store it in task.embedding for later semantic search.
    return task
