from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from models import Discipline
import peewee

app = FastAPI(title="Discipline Service")


# Схемы валидации
class DisciplineCreate(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=255)
    is_active: Optional[bool] = True


class DisciplineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = None
    is_active: Optional[bool] = None


# Эндпоинты
@app.post("/disciplines/")
def create_discipline(d: DisciplineCreate):
    try:
        new_disc = Discipline.create(name=d.name, code=d.code, is_active=d.is_active)
        return {"id": new_disc.id, "name": new_disc.name, "code": new_disc.code}
    except peewee.IntegrityError:
        raise HTTPException(
            status_code=400, detail="Дисциплина с таким именем и кодом уже существует"
        )


@app.put("/disciplines/{disc_id}")
def update_discipline(disc_id: int, d: DisciplineUpdate):
    disc = Discipline.get_or_none(Discipline.id == disc_id)
    if not disc:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")

    if d.name:
        disc.name = d.name
    if d.code:
        disc.code = d.code
    if d.is_active is not None:
        disc.is_active = d.is_active

    disc.save()
    return {"id": disc.id, "status": "updated"}


@app.delete("/disciplines/{disc_id}")
def delete_discipline(disc_id: int):
    # Используем новый метод из модели, который возвращает True/False
    result = Discipline.close(disc_id)
    return result


@app.get("/disciplines/{disc_id}")
def get_discipline(disc_id: int):
    disc = Discipline.get_or_none(Discipline.id == disc_id)
    if not disc:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    return {
        "id": disc.id,
        "name": disc.name,
        "code": disc.code,
        "is_active": disc.is_active,
    }


@app.get("/disciplines")
def get_list(name: Optional[str] = None, is_active: Optional[bool] = None):
    query = Discipline.select()
    if name:
        query = query.where(Discipline.name.contains(name))
    if is_active is not None:
        query = query.where(Discipline.is_active == is_active)

    return [
        {"id": d.id, "name": d.name, "code": d.code, "is_active": d.is_active}
        for d in query
    ]
