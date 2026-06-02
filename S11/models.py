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
        database = db
        # Исправленный синтаксис составного уникального индекса Peewee
        indexes = ((('name', 'code'), True),)

    @classmethod
    def add_discipline(cls, name: str, code: str, is_active: bool = True):
        """Добавление дисциплины с возвратом id, name, code и валидацией уникальности"""
        if len(name) > 255 or len(code) > 255:
            raise ValueError("Превышена максимальная длина поля (max 255)")
        try:
            new_disc = cls.create(name=name, code=code, is_active=is_active)
            return {"id": new_disc.id, "name": new_disc.name, "code": new_disc.code}
        except IntegrityError:
            raise ValueError("Дисциплина с таким именем и кодом уже существует")

    @classmethod
    def update_discipline_by_id(cls, discipline_id: int, name: str = None, code: str = None, is_active: bool = None):
        """Изменение дисциплины по ID с возвратом id и status"""
        discipline = cls.get_or_none(cls.id == discipline_id)
        if not discipline:
            return None
        
        has_changes = False
        if name is not None:
            if len(name) > 255:
                raise ValueError("Превышена максимальная длина поля name (max 255)")
            if discipline.name != name:
                discipline.name = name
                has_changes = True
        if code is not None:
            if len(code) > 255:
                raise ValueError("Превышена максимальная длина поля code (max 255)")
            if discipline.code != code:
                discipline.code = code
                has_changes = True
        if is_active is not None and discipline.is_active != is_active:
            discipline.is_active = is_active
            has_changes = True
            
        if has_changes:
            try:
                discipline.save()
            except IntegrityError:
                raise ValueError("Дисциплина с такой комбинацией имени и кода уже существует")
                
        return {"id": discipline.id, "status": "updated"}

    @classmethod
    def delete_discipline_by_id(cls, discipline_id: int):
        """Удаление дисциплины по ID"""
        discipline = cls.get_or_none(cls.id == discipline_id)
        if discipline and discipline.is_active:
            discipline.is_active = False
            discipline.save()
            return True
        return False

    @classmethod
    def get_discipline_by_id(cls, discipline_id: int):
        """Получение дисциплины по ID"""
        discipline = cls.get_or_none(cls.id == discipline_id)
        if not discipline:
            return None
        return {
            "id": discipline.id,
            "name": discipline.name,
            "code": discipline.code,
            "is_active": discipline.is_active
        }

    @classmethod
    def get_disciplines_list(cls, name: str = None, is_active: bool = None):
        """Получение списка дисциплин по параметрам"""
        query = cls.select()
        if name:
            query = query.where(cls.name == name)  # Изменено с .contains на точное совпадение по требованию ИИ
        if is_active is not None:
            query = query.where(cls.is_active == is_active)
        return [
            {"id": d.id, "name": d.name, "code": d.code, "is_active": d.is_active}
            for d in query
        ]

def init_db():
    """Инициализация базы данных и создание таблиц"""
    db.connect()
    db.create_tables([Discipline], safe=True)
    print("Таблица Discipline создана.")

if __name__ == "__main__":
    init_db()
