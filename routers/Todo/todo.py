from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas.Todo.schema as schemas
import routers.Todo.todoscrud as todoscrud
from database import SessionLocal

router = APIRouter(
    prefix="/todo"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = todoscrud.create_todo(db, todo)
    return todo


@router.get("", response_model=List[schemas.ToDoResponse])
def get_todo(completed: bool = None, db: Session = Depends(get_db)):
    todo = todoscrud.read_todos(db, completed)
    return todo


@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = todoscrud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo


@router.put("/{id}")
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = todoscrud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = todoscrud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")
