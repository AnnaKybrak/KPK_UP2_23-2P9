from peewee import *

db = SqliteDatabase('disciplines.db')

class BaseModel(Model):
    class Meta:
        database = db

class Discipline(BaseModel):
    """Модель справочника дисциплин"""
    name = CharField(max_length=255, unique=True, null=False)
    code = CharField(unique=True, null=False)
    is_active = BooleanField(default=True, null=False)

def init_db():
    """Инициализация базы данных и создание таблиц"""
    db.connect()
    db.create_tables([Discipline], safe=True)
    print("Таблица Discipline создана.")

if __name__ == "__main__":
    init_db()