from sqlalchemy.orm import Session

from catalog import schemas

from catalog.db import models


def get_all_cheese_types(db: Session):
    return db.query(models.DBCheeseType).all()


def get_cheese_type(db: Session, cheese_type_id: int):
    return (
        db.query(models.DBCheeseType)
        .filter(models.DBCheeseType.id == cheese_type_id)
        .first()
    )


def get_cheese_type_by_name(db: Session, name: str):
    return (
        db.query(models.DBCheeseType).filter(models.DBCheeseType.name == name).first()
    )


def create_cheese_type(db: Session, cheese_type: schemas.CheeseTypeCreate):
    db_cheese_type = models.DBCheeseType(
        name=cheese_type.name, description=cheese_type.description
    )
    db.add(db_cheese_type)
    db.commit()
    db.refresh(db_cheese_type)
    return db_cheese_type


def get_cheese_list(db: Session):
    return db.query(models.DBCheese).all()


def create_cheese(db: Session, cheese: schemas.CheeseCreate):
    db_cheese = models.DBCheese(
        title=cheese.title,
        price=cheese.price,
        packaging_type=cheese.packaging_type,
        cheese_type_id=cheese.cheese_type_id,
    )
    db.add(db_cheese)
    db.commit()
    db.refresh(db_cheese)
    return db_cheese
