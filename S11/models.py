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

    def delete_instance(self, recursive=False, delete_nullable=False):
        self.is_active = False
        self.save()
        return 1

def init_db():
    """Инициализация базы данных и создание таблиц"""
    db.connect()
    db.create_tables([Discipline], safe=True)
    print("Таблица Discipline создана.")

if __name__ == "__main__":
    init_db()