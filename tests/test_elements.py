from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import text
from app.security import create_access_token
from decimal import Decimal

client = TestClient(app)


def test_get_elements():
     response = client.get("/elements")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     if json_data:
          assert "ElementId" in json_data[0]
          
def test_get_element_success(element):
     element_id = element
     response = client.get(f"/elements/{element_id}")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, dict)
     assert "ElementId" in json_data
     assert json_data["Name"] == "Test element"
     
def test_get_element_not_found():
     response = client.get("/elements/9999999")
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_get_elements_without_calculations(element):
     element_id = element
     response = client.get("/elements/without-calcs")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     element_id_list = [item["ElementId"] for item in json_data]
     assert element_id in element_id_list
          
def test_get_latest_calculation_success(calculation, db):
     element_id, calculation_id = calculation
     response = client.get(
          f"/elements/{element_id}/calculations/latest"
     )
     assert response.status_code == 200
     json_data = response.json()
     assert json_data["CalculationId"] == calculation_id
     assert json_data["ElementId"] == element_id
     result = db.execute(
          text("""
               SELECT
                    CalculationId,
                    ElementId,
                    BendingMoment,
                    AxialForce,
                    LoadValue,
                    LoadCapacityFactor
               FROM Calculation
               WHERE ElementId = :element_id;
          """),
          {"element_id": element_id}
     )
     row = result.fetchone()
     assert(
          row.CalculationId == calculation_id
          and row.ElementId == element_id
          and row.BendingMoment == Decimal("100.00")
          and row.AxialForce == Decimal("50.00")
          and row.LoadValue == Decimal("80.00")
          and row.LoadCapacityFactor == Decimal("0.80")
     )
     
def test_get_latest_calculation_not_found(element):
     element_id = element
     response = client.get(
          f"/elements/{element_id}/calculations/latest"
     )
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_get_latest_element_not_found():
     response = client.get(
          "/elements/9999999/calculations/latest"
     )
     assert response.status_code == 404
          
def test_create_element_success(regular_user, project, element_type, db):
     project_id = project
     element_type_id = element_type
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/elements",
          json={
               "ProjectId": project_id,
               "ElementTypeId": element_type_id,
               "Name": "Test element",
               "Dimensions": "100x100",
               "TechnicalParameters": "Test parameters"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 201
     json_data = response.json()
     assert isinstance(json_data, dict)
     assert "ElementId" in json_data
     assert "successfully" in json_data["message"]
     element_id = json_data["ElementId"]
     try:
          result = db.execute(
               text("""
                         SELECT Name FROM StructuralElement
                         WHERE ElementId = :element_id
                    """),
               {"element_id": element_id}
          )
          test_name = result.scalar()
          assert test_name == "Test element"
     finally:
          db.execute(
               text("""
                         DELETE FROM StructuralElement
                         WHERE ElementId = :element_id
                    """),
               {"element_id": element_id}
          )
          db.commit()
     
def test_create_element_project_not_found(regular_user, element_type):
     element_type_id = element_type
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/elements",
          json={
               "ProjectId": 99999999,
               "ElementTypeId": element_type_id,
               "Name": "Test Element",
               "Dimensions": "100x100mm",
               "TechnicalParameters": "Test Parameters"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_create_element_without_authentication(project, element_type):
     project_id = project
     element_type_id = element_type
     response = client.post(
          "/elements",
          json={
               "ProjectId": project_id,
               "ElementTypeId": element_type_id,
               "Name": "Test element",
               "Dimensions": "100x100",
               "TechnicalParameters": "Test parameters"
          }
     )
     assert response.status_code == 401
     
def test_create_element_invalid_token(project, element_type):
     project_id = project
     element_type_id = element_type
     token = create_access_token(
          data={"sub": "99999999"}
     )
     response = client.post(
          "/elements",
          json={
               "ProjectId": project_id,
               "ElementTypeId": element_type_id,
               "Name": "Test element",
               "Dimensions": "100x100",
               "TechnicalParameters": "Test parameters"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 401
     
def test_update_element_dimensions_success(regular_user, element, db):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     element_id = element
     response = client.put(
          f"/elements/{element_id}/dimensions?new_dimensions=200x300",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT Dimensions FROM StructuralElement
               WHERE ElementId = :element_id    
          """),
          {"element_id": element_id}
     )
     dimensions = result.scalar()
     assert dimensions == "200x300"
     
def test_update_element_dimensions_without_authentication(element):
     element_id = element
     response = client.put(
          f"/elements/{element_id}/dimensions?new_dimensions=200x300"
     )
     assert response.status_code == 401
     
def test_update_element_dimensions_not_found(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          "/elements/9999999/dimensions?new_dimensions=200x300",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_delete_element_without_authentication(element):
     element_id = element
     response = client.delete(
          f"/elements/{element_id}"
     )
     assert response.status_code == 401
     
def test_delete_element_without_admin_role(regular_user, element):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     element_id = element
     response = client.delete(
          f"/elements/{element_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 403
     
def test_delete_element_admin_element_not_found(admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.delete(
          "/elements/99999999",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_delete_element_success(admin_user, element, db):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     element_id = element
     response = client.delete(
          f"/elements/{element_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 204
     query = db.execute(
          text("""
               SELECT ElementId FROM StructuralElement
               WHERE ElementId = :element_id;     
          """),
          {"element_id": element_id}
     )
     result = query.scalar()
     assert result is None