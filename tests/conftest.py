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
     element_id = 2
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
                    :element_id,
                    2,
                    2,
                    22
               );
          """),
          {"element_id": element_id}
     )
     material_usage_id = result.scalar()
     db.commit()
     
     try:
          yield material_usage_id, element_id
     finally:
          db.execute(
               text("""
                    DELETE FROM MaterialUsage
                    WHERE MaterialUsageId = :material_usage_id
               """),
               {"material_usage_id": material_usage_id}
          )
          db.commit()
          
@pytest.fixture
def element(db):
     params = {
          "ProjectId": 1,
          "ElementTypeId": 1,
          "Name": "Test element",
          "Dimensions": "100x100",
          "TechnicalParameters": "Test parameters"
     }
     result = db.execute(
          text("""
               EXEC sp_AddStructuralElement
                    @ProjectId = :ProjectId,
                    @ElementTypeId = :ElementTypeId,
                    @Name = :Name,
                    @Dimensions = :Dimensions,
                    @TechnicalParameters = :TechnicalParameters; 
          """),
          params
     )
     element_id = result.scalar()
     db.commit()
     
     try:
          yield element_id
     finally:
          db.execute(
               text("""
                    DELETE FROM StructuralElement
                    WHERE ElementId = :element_id;
               """),
               {"element_id": element_id}
          )
          db.commit()