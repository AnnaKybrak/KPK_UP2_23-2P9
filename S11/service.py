from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models import Discipline, db

app = FastAPI(title="Discipline Service")

# Схемы для валидации данных (API)
class DisciplineCreate(BaseModel):
    name: str
    code: str

class DisciplineUpdate(BaseModel):
    name: str = None
    code: str = None
    is_active: bool = None

# Подключение к БД при старте и закрытие при выключении
@app.on_event("startup")
def startup():
    if db.is_closed():
        db.connect()

@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()

@app.post("/disciplines")
def create_discipline(discipline: DisciplineCreate):
    try:
        new_disc = Discipline.create(name=discipline.name, code=discipline.code)
        return {"id": new_disc.id, "name": new_disc.name}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Дисциплина с таким именем или кодом уже существует")

@app.put("/disciplines/{disc_id}")
def update_discipline(disc_id: int, data: DisciplineUpdate):
    try:
        disc = Discipline.get_by_id(disc_id)
        if data.name is not None:
            disc.name = data.name
        if data.code is not None:
            disc.code = data.code
        if data.is_active is not None:
            disc.is_active = data.is_active
        disc.save()
        return {"id": disc.id, "status": "updated"}
    except Discipline.DoesNotExist:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")

@app.delete("/disciplines/{disc_id}")
def delete_discipline(disc_id: int):
    try:
        disc = Discipline.get_by_id(disc_id)
        disc.is_active = False
        disc.save()
        return True
    except Discipline.DoesNotExist:
        return False

@app.get("/disciplines/{disc_id}")
def get_discipline(disc_id: int):
    try:
        disc = Discipline.get_by_id(disc_id)
        return {"id": disc.id, "name": disc.name, "code": disc.code, "is_active": disc.is_active}
    except Discipline.DoesNotExist:
        raise HTTPException(status_code=404, detail="Дисциплина не найдена")