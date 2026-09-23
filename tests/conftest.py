import pytest
from app.database import SessionLocal, get_db
from app.main import app
from sqlalchemy import text
from datetime import date


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
def project(db):
     params = {
          "ProjectName": "Test Name",
          "Scope": "Test Scope",
          "Location": "Test Location",
          "Status": "Nowy",
          "DueDate": date(2030, 9, 30)
     }
     result = db.execute(
          text("""
               INSERT INTO Project
               (
                    ProjectName,
                    Scope,
                    Location,
                    Status,
                    DueDate,
                    CreatedAt
               )
               OUTPUT INSERTED.ProjectId
               VALUES
               (
                    :ProjectName,
                    :Scope,
                    :Location,
                    :Status,
                    :DueDate,
                    GETDATE()
               )
          """),
          params
     )
     project_id = result.scalar()
     db.commit()
     try:
          yield project_id
     finally:
          db.execute(
               text("""
                    DELETE FROM Project
                    WHERE ProjectId = :project_id
               """),
               {"project_id": project_id}
          )
          db.commit()

@pytest.fixture
def material_type(db):
     material_type_name = "Test material type"
     result = db.execute(
          text("""
               INSERT INTO MaterialType (Name)     
               OUTPUT INSERTED.MaterialTypeId
               VALUES (:name)
          """),
          {"name": material_type_name}
     )
     material_type_id = result.scalar()
     db.commit()
     try:
          yield material_type_id
     finally:
          db.execute(
               text("""
                    DELETE FROM MaterialType
                    WHERE MaterialTypeId = :material_type_id     
               """),
               {"material_type_id": material_type_id}
          )
          db.commit()
   
@pytest.fixture
def material(material_type, db):
     material_type_id = material_type
     material_name = "Test material"
     result = db.execute(
          text("""
               INSERT INTO Material (Name, MaterialTypeId)
               OUTPUT INSERTED.MaterialId
               VALUES (:name, :material_type_id)
          """),
          {
               "name": material_name,
               "material_type_id": material_type_id
          }
     )
     material_id = result.scalar()
     db.commit()
     try:
          yield material_id
     finally:
          db.execute(
               text("""
                    DELETE FROM Material
                    WHERE MaterialId = :material_id     
               """),
               {"material_id": material_id}
          )
          db.commit()
          
@pytest.fixture
def unit(db):
     params = {
          "Name": "Test unit",
          "Symbol": "TU"
     }
     result = db.execute(
          text("""
               INSERT INTO Unit (Name, Symbol)
               OUTPUT INSERTED.UnitId
               VALUES (:Name, :Symbol)
          """),
          params
     )
     unit_id = result.scalar()
     db.commit()
     try:
          yield unit_id
     finally:
          db.execute(
               text("""
                    DELETE FROM Unit
                    WHERE UnitId = :unit_id     
               """),
               {"unit_id": unit_id}
          )
          db.commit()

@pytest.fixture
def material_unit(material, unit, db):
     material_id = material
     unit_id = unit
     db.execute(
          text("""
               INSERT INTO MaterialUnit (MaterialId, UnitId)
               VALUES (:material_id, :unit_id)     
          """),
          {
               "material_id": material_id,
               "unit_id": unit_id
          }
     )
     db.commit()
     try:
          yield material_id, unit_id
     finally:
          db.execute(
               text("""
                    DELETE FROM MaterialUnit
                    WHERE MaterialId = :material_id
                    AND UnitId = :unit_id     
               """),
               {
                    "material_id": material_id,
                    "unit_id": unit_id
               }
          )
          db.commit()

@pytest.fixture
def element_type(db):
     element_type_name = "Test element type"
     result = db.execute(
          text("""
               INSERT INTO ElementType
               OUTPUT INSERTED.ElementTypeId
               VALUES (:name)     
          """),
          {"name": element_type_name}
     )
     element_type_id = result.scalar()
     db.commit()
     try:
          yield element_type_id
     finally:
          db.execute(
               text("""
                    DELETE FROM ElementType
                    WHERE ElementTypeId = :element_type_id     
               """),
               {"element_type_id": element_type_id}
          )
          db.commit()

@pytest.fixture
def element(project, element_type, db):
     project_id = project
     element_type_id = element_type
     params = {
          "ProjectId": project_id,
          "ElementTypeId": element_type_id,
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

@pytest.fixture
def material_usage(element, material_unit, db):
     element_id = element
     material_id, unit_id = material_unit
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
                    :material_id,
                    :unit_id,
                    22
               );
          """),
          {
               "element_id": element_id,
               "material_id": material_id,
               "unit_id": unit_id
          }
     )
     material_usage_id = result.scalar()
     db.commit()
     try:
          yield material_usage_id, element_id, material_id
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
def admin_user(db):
     params = {
          "FirstName": "Test",
          "LastName": "Test",
          "Email": "test123@test.com",
          "Role": "ADMIN",
          "IsActive": 1,
          "PasswordHash": "test123"
     }
     result = db.execute(
          text("""
               INSERT INTO [User]
               (
                    FirstName,
                    LastName,
                    Email,
                    Role,
                    IsActive,
                    CreatedAt,
                    PasswordHash
               )
               OUTPUT INSERTED.UserId
               VALUES
               (
                    :FirstName,
                    :LastName,
                    :Email,
                    :Role,
                    :IsActive,
                    GETDATE(),
                    :PasswordHash
               )
          """),
          params
     )
     user_id = result.scalar()
     db.commit()
     try:
          yield user_id
     finally:
          db.execute(
               text("""
                    DELETE FROM [User]
                    WHERE UserId = :user_id
               """),
               {"user_id": user_id}
          )
          db.commit()
          
@pytest.fixture
def regular_user(db):
     params = {
          "FirstName": "Test",
          "LastName": "Test",
          "Email": "test123@test.com",
          "Role": "ASYSTENT",
          "IsActive": 1,
          "PasswordHash": "test123"
     }
     result = db.execute(
          text("""
               INSERT INTO [User]
               (
                    FirstName,
                    LastName,
                    Email,
                    Role,
                    IsActive,
                    CreatedAt,
                    PasswordHash
               )
               OUTPUT INSERTED.UserId
               VALUES
               (
                    :FirstName,
                    :LastName,
                    :Email,
                    :Role,
                    :IsActive,
                    GETDATE(),
                    :PasswordHash
               )
          """),
          params
     )
     user_id = result.scalar()
     db.commit()
     try:
          yield user_id
     finally:
          db.execute(
               text("""
                    DELETE FROM [User]
                    WHERE UserId = :user_id
               """),
               {"user_id": user_id}
          )
          db.commit()
          
@pytest.fixture
def calculation(element, db):
     params = {
          "ElementId": element,
          "BendingMoment": 100.00,
          "AxialForce": 50.00,
          "LoadValue": 80.00,
          "LoadCapacityFactor": 0.80
     }
     db.execute(
          text("""
               EXEC sp_AddCalculations
               @ElementId = :ElementId,
               @BendingMoment = :BendingMoment,
               @AxialForce = :AxialForce,
               @LoadValue = :LoadValue,
               @LoadCapacityFactor = :LoadCapacityFactor
          """),
          params
     )
     result = db.execute(
          text("""
               SELECT TOP 1 CalculationId
               FROM Calculation
               WHERE ElementId = :element_id
               ORDER BY CalculationId DESC     
          """),
          {"element_id": element}
     )
     calculation_id = result.scalar()
     db.commit()
     try:
          yield element, calculation_id
     finally:
          db.execute(
               text("""
                    DELETE FROM Calculation
                    WHERE ElementId = :element     
               """),
               {"element": element}
          )
          db.commit()