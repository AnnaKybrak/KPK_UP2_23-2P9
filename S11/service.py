from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from models import Discipline

app = FastAPI(title="Discipline Service")


class DisciplineCreate(BaseModel):
    name: str = Field(..., max_length=255)
    code: str = Field(..., max_length=255)
    is_active: Optional[bool] = True


class DisciplineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = None
    is_active: Optional[bool] = None


@app.post("/disciplines/")
def create_discipline(d: DisciplineCreate):
    try:
        return Discipline.add_discipline(
            name=d.name, code=d.code, is_active=d.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/disciplines/{disc_id}")
def update_discipline(disc_id: int, d: DisciplineUpdate):
    try:
        result = Discipline.update_by_id(
            discipline_id=disc_id, name=d.name, code=d.code, is_active=d.is_active
        )
        if not result:
            raise HTTPException(status_code=404, detail="Дисциплина не найдена")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/disciplines/{disc_id}")
def delete_discipline(disc_id: int):
    return Discipline.delete_discipline_by_id(disc_id)


@app.get("/disciplines/{disc_id}")
def get_discipline(disc_id: int):
    result = Discipline.get_discipline_by_id(disc_id)
    if not result:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")
    return result


@app.get("/disciplines")
def get_list(name: Optional[str] = None, is_active: Optional[bool] = None):
    return Discipline.get_disciplines_list(name=name, is_active=is_active)
