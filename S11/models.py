from peewee import *

db = SqliteDatabase('disciplines.db')

class BaseModel(Model):
    class Meta:
        database = db

class Discipline(BaseModel):
    """Модель справочника дисциплин"""
    id = PrimaryKeyField()
    name = CharField(max_length=255) 
    code = CharField(max_length=255) 
    is_active = BooleanField(default=True)

    class Meta:
        indexes = (
            (('name', 'code'), True),
        )

    @classmethod
    def close(cls, discipline_id):
        discipline = cls.get_or_none(cls.id == discipline_id)
        if discipline and discipline.is_active:
            discipline.is_active = False
            discipline.save()
            return True
        return False

def init_db():
    """Инициализация базы данных и создание таблиц"""
    db.connect()
    db.create_tables([Discipline], safe=True)
    print("Таблица Discipline создана.")

if __name__ == "__main__":
    init_db()