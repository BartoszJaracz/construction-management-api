import pytest
from app.database import SessionLocal, get_db
from app.main import app
from sqlalchemy import text


@pytest.fixture
def db():
     db = SessionLocal()
     
     def override_get_db():
          yield db
     
     app.dependency_overrides[get_db] = override_get_db
     
     try:
          yield db
     finally:
          db.rollback()
          db.close()
          app.dependency_overrides.clear()
          
@pytest.fixture
def material_usage(db):
     result = db.execute(
          text("""
               INSERT INTO MaterialUsage
               (
                    ElementId,
                    MaterialId,
                    UnitId,
                    Quantity
               )
               OUTPUT INSERTED.MaterialUsageId
               VALUES
               (
                    2,
                    2,
                    2,
                    22
               );
          """)
     )
     material_usage_id = result.scalar()
     db.commit()
     
     try:
          yield material_usage_id
     finally:
          db.execute(
               text("""
                    DELETE FROM MaterialUsage
                    WHERE MaterialUsageId = :material_usage_id
               """),
               {"material_usage_id": material_usage_id}
          )
          
          db.commit()