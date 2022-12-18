import Models.models as models
from Database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()