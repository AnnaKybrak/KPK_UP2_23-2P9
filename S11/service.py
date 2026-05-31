from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from models import Discipline
import uvicorn

app = FastAPI(title="Discipline Service")


class DisciplineCreate(BaseModel):
    name: str = Field(..., max_length=255)
    code: str
    is_active: Optional[bool] = True


class DisciplineUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = None
    is_active: Optional[bool] = None


@app.post("/disciplines/")
def create_discipline(d: DisciplineCreate):
    new_disc = Discipline.create(name=d.name, code=d.code, is_active=d.is_active)
    return {"id": new_disc.id, "name": new_disc.name, "code": new_disc.code}


@app.put("/disciplines/{disc_id}")
def update_discipline(disc_id: int, d: DisciplineUpdate):
    disc = Discipline.get_or_none(Discipline.id == disc_id)
    if not disc:
        raise HTTPException(status_code=404, detail="Not found")
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
    disc = Discipline.get_or_none(Discipline.id == disc_id)
    if not disc:
        return False
    disc.is_active = False
    disc.save()
    return True


@app.get("/disciplines/{disc_id}")
def get_discipline(disc_id: int):
    disc = Discipline.get_or_none(Discipline.id == disc_id)
    if not disc:
        raise HTTPException(status_code=404, detail="Not found")
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
