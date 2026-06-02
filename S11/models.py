from peewee import *

db = SqliteDatabase("disciplines.db")


class BaseModel(Model):
    class Meta:
        database = db


class Discipline(BaseModel):
    """Модель справочника дисциплин"""

    name = CharField(max_length=255)
    code = CharField(max_length=255)
    is_active = BooleanField(default=True)

    class Meta:
        indexes = ((("name", "code"), True),)

    @classmethod
    def add_discipline(cls, name: str, code: str, is_active: bool = True):
        existing = cls.get_or_none((cls.name == name) & (cls.code == code))
        if existing:
            raise ValueError("Дисциплина с таким именем и кодом уже существует")

        try:
            new_disc = cls.create(name=name, code=code, is_active=is_active)
            return {"id": new_disc.id, "name": new_disc.name, "code": new_disc.code}
        except IntegrityError:
            raise ValueError("Ошибка БД: нарушение уникальности")

    @classmethod
    def update_by_id(
        cls,
        discipline_id: int,
        name: str = None,
        code: str = None,
        is_active: bool = None,
    ):
        discipline = cls.get_or_none(cls.id == discipline_id)
        if not discipline:
            return None

        new_name = name if name is not None else discipline.name
        new_code = code if code is not None else discipline.code

        if (name is not None and name != discipline.name) or (
            code is not None and code != discipline.code
        ):
            existing = cls.get_or_none((cls.name == new_name) & (cls.code == new_code))
            if existing and existing.id != discipline.id:
                raise ValueError("Комбинация name и code должна быть уникальной")

        if name is not None:
            discipline.name = name
        if code is not None:
            discipline.code = code
        if is_active is not None:
            discipline.is_active = is_active

        try:
            discipline.save()
            return {"id": discipline.id, "status": "updated"}
        except IntegrityError:
            raise ValueError("Ошибка БД при обновлении: нарушение уникальности")

    @classmethod
    def delete_discipline_by_id(cls, discipline_id: int):
        discipline = cls.get_or_none(cls.id == discipline_id)
        if discipline is None:
            return False
        if discipline.is_active:
            discipline.is_active = False
            discipline.save()
            return True
        return False

    @classmethod
    def get_discipline_by_id(cls, discipline_id: int):
        discipline = cls.get_or_none(cls.id == discipline_id)
        if not discipline:
            return None
        return {
            "id": discipline.id,
            "name": discipline.name,
            "code": discipline.code,
            "is_active": discipline.is_active,
        }

    @classmethod
    def get_disciplines_list(cls, name: str = None, is_active: bool = None):
        query = cls.select()
        if name:
            query = query.where(cls.name.contains(name))
        if is_active is not None:
            query = query.where(cls.is_active == is_active)

        query = query.order_by(cls.id)

        return [
            {"id": d.id, "name": d.name, "code": d.code, "is_active": d.is_active}
            for d in query
        ]


def init_db():
    db.connect()
    db.create_tables([Discipline], safe=True)
    print("Таблица Discipline создана.")


if __name__ == "__main__":
    init_db()
