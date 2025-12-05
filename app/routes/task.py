from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select, and_

from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import ReadTask, CreateTask, UpdateTask
from app.utilities.database import get_db_session
from app.utilities.helper import get_utc_now
from app.utilities.logger import get_logger
from app.utilities.security import get_current_user

task_router = APIRouter()
logger = get_logger(__name__)


@task_router.post("/create", response_model=ReadTask, status_code=201)
def create_task(
    task: CreateTask,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> ReadTask:
    try:
        new_task = Task(
            title=task.title.strip(),
            description=task.description.strip() if task.description else None,
            note=task.note.strip() if task.note else None,
            status=TaskStatus.PENDING,
            owner_id=user.id,
        )

        db_session.add(new_task)
        db_session.commit()
        db_session.refresh(new_task)

        logger.info(f"New task created with ID: {new_task.id}")

        return new_task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during task creation")
        raise HTTPException(status_code=500, detail="Failed to create task")


@task_router.get("/list", response_model=list[ReadTask], status_code=200)
def list_tasks(
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> list[ReadTask]:
    try:
        tasks = db_session.exec(
            select(Task).where(and_(Task.owner_id == user.id, Task.is_active == True))  # noqa
        ).all()

        logger.info(f"Total active tasks {len(tasks)}")
        return tasks if tasks else []  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during active task listing")
        raise HTTPException(status_code=500, detail="Failed to list active tasks")


def get_task_by_id(task_id: int, db_session: Session, user_id: int) -> ReadTask:
    try:
        task = db_session.exec(
            select(Task).where(
                and_(
                    Task.owner_id == user_id, Task.id == task_id, Task.is_active == True
                )
            )  # noqa
        ).one_or_none()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during task retrieval")
        raise HTTPException(status_code=500, detail="Failed to retrieve task")


@task_router.get("/get/{task_id}", response_model=ReadTask, status_code=200)
def get_task(
    task_id: int,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> ReadTask:
    try:
        db_task = get_task_by_id(task_id, db_session, user.id)

        logger.info(f"Task retrieved with ID: {db_task.id}")
        return db_task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Unable to fetch tasks:{task_id} at this time.")
        raise HTTPException(
            status_code=500,
            detail="Tasks could not be loaded at the moment. Please refresh.",
        )


@task_router.put("/update/{task_id}", response_model=ReadTask, status_code=200)
def update_task(
    task_id: int,
    task: UpdateTask,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> ReadTask:
    try:
        db_task = get_task_by_id(task_id, db_session, user.id)

        if task.title is None:
            raise HTTPException(
                status_code=400, detail="Missing required fields for full update"
            )

        db_task.title = task.title.strip()
        db_task.description = task.description.strip() if task.description else None
        db_task.note = task.note.strip() if task.note else None
        db_task.updated_at = get_utc_now()

        db_session.add(db_task)
        db_session.commit()
        db_session.refresh(db_task)

        logger.info(f"Task updated with ID: {db_task.id}")
        return db_task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Unable to fetch tasks:{task_id} at this time.")
        raise HTTPException(
            status_code=500,
            detail="Tasks could not be loaded at the moment. Please refresh.",
        )


@task_router.patch("/edit/{task_id}", response_model=ReadTask, status_code=200)
def edit_task(
    task_id: int,
    task: UpdateTask,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> ReadTask:
    try:
        db_task = get_task_by_id(task_id, db_session, user.id)

        if task.title is not None:
            db_task.title = task.title.strip()
        if task.description is not None:
            db_task.description = task.description.strip()
        if task.note is not None:
            db_task.note = task.note.strip()

        db_task.updated_at = get_utc_now()

        db_session.add(db_task)
        db_session.commit()
        db_session.refresh(db_task)

        logger.info(f"Task edited with ID: {db_task.id}")
        return db_task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Unable to fetch tasks:{task_id} at this time.")
        raise HTTPException(
            status_code=500,
            detail="Tasks could not be loaded at the moment. Please refresh.",
        )


@task_router.delete("/delete/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> None:
    try:
        db_task = get_task_by_id(task_id, db_session, user.id)

        db_task.is_active = False
        db_task.updated_at = get_utc_now()

        db_session.add(db_task)
        db_session.commit()

        logger.info(f"Task deleted with ID: {db_task.id}")

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Unable to delete tasks:{task_id} at this time.")
        raise HTTPException(
            status_code=500,
            detail="Tasks could not be deleted at the moment. Please try again.",
        )


@task_router.get("/list/deleted", response_model=list[ReadTask], status_code=200)
def list_deleted_tasks(
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> list[ReadTask]:
    try:
        tasks = db_session.exec(
            select(Task).where(and_(Task.owner_id == user.id, Task.is_active == False))  # noqa
        ).all()

        logger.info(f"Total deleted tasks {len(tasks)}")
        return tasks if tasks else []  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception("Unexpected error during deleted task listing")
        raise HTTPException(status_code=500, detail="Failed to list deleted tasks")


@task_router.patch("/activate/{task_id}", status_code=200)
def activate_task(
    task_id: int,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> ReadTask:
    try:
        db_task = db_session.exec(
            select(Task).where(
                and_(
                    Task.owner_id == user.id,
                    Task.id == task_id,
                    Task.is_active == False,
                )
            )  # noqa
        ).one_or_none()

        if not db_task:
            raise HTTPException(status_code=404, detail="Task not deleted or notfound")

        db_task.is_active = True
        db_task.updated_at = get_utc_now()

        db_session.add(db_task)
        db_session.commit()

        logger.info(f"Task active with ID: {db_task.id}")
        return db_task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Unable to active tasks:{task_id} at this time.")
        raise HTTPException(
            status_code=500,
            detail="Tasks could not be active at the moment. Please try again.",
        )


@task_router.patch("/status/{task_id}", status_code=200)
def change_task_status(
    task_id: int,
    status: TaskStatus,
    db_session: Session = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> ReadTask:
    try:
        db_task = get_task_by_id(task_id, db_session, user.id)

        if db_task.status == status:
            raise HTTPException(
                status_code=400, detail="Task status is already the same"
            )

        db_task.status = status
        db_task.updated_at = get_utc_now()

        db_session.add(db_task)
        db_session.commit()
        db_session.refresh(db_task)

        logger.info(f"Task status changed with ID: {db_task.id}")
        return db_task  # noqa

    except HTTPException:
        raise
    except Exception:
        logger.exception(f"Unable to change task status:{task_id} at this time.")
        raise HTTPException(
            status_code=500,
            detail="Task status could not be changed at the moment. Please try again.",
        )
