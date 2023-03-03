from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from catalog import schemas
from catalog import crud
from catalog.db.engine import SessionLocal

app = FastAPI()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/cheese_types/", response_model=list[schemas.CheeseType])
async def read_cheese_types(db: Session = Depends(get_db)):
    return crud.get_all_cheese_types(db=db)


@app.post("/cheese_types/", response_model=schemas.CheeseType)
async def create_cheese_type(
    cheese_type: schemas.CheeseTypeCreate, db: Session = Depends(get_db)
):
    db_cheese_type = crud.get_cheese_type_by_name(db=db, name=cheese_type.name)

    if db_cheese_type:
        raise HTTPException(
            status_code=400, detail="Such name for CheeseType already exists"
        )

    return crud.create_cheese_type(db=db, cheese_type=cheese_type)


@app.get("/cheese/", response_model=list[schemas.Cheese])
async def read_cheese(db: Session = Depends(get_db)):
    return crud.get_cheese_list(db)


@app.post("/cheese/", response_model=schemas.Cheese)
async def create_cheese(cheese: schemas.CheeseCreate, db: Session = Depends(get_db)):
    return crud.create_cheese(db=db, cheese=cheese)
