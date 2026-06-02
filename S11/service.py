from fastapi import FastAPI, HTTPException, status
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
    code: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

@app.post("/disciplines/", status_code=status.HTTP_201_CREATED)
def create_discipline(d: DisciplineCreate):
    try:
        return Discipline.add_discipline(name=d.name, code=d.code, is_active=d.is_active)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.put("/disciplines/{disc_id}", status_code=status.HTTP_200_OK)
def update_discipline(disc_id: int, d: DisciplineUpdate):
    try:
        result = Discipline.update_by_id(
            discipline_id=disc_id, 
            name=d.name, 
            code=d.code, 
            is_active=d.is_active
        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Дисциплина не найдена")
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete("/disciplines/{disc_id}", status_code=status.HTTP_200_OK)
def delete_discipline(disc_id: int):
    result = Discipline.delete_discipline_by_id(disc_id)
    if result is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Дисциплина не найдена или уже удалена")
    return result

@app.get("/disciplines/{disc_id}", status_code=status.HTTP_200_OK)
def get_discipline(disc_id: int):
    result = Discipline.get_discipline_by_id(disc_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Дисциплина не найдена")
    return result

@app.get("/disciplines", status_code=status.HTTP_200_OK)
def get_list(name: Optional[str] = None, is_active: Optional[bool] = None):
    return Discipline.get_disciplines_list(name=name, is_active=is_active)