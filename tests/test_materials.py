from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import text
from app.security import create_access_token

client = TestClient(app)


def test_get_material_success():
     response = client.get("/materials")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance (json_data, list)
     assert json_data
     first_element = json_data[0]
     assert isinstance(first_element, dict)
     assert "MaterialId" in first_element

def test_get_material_usage_not_found():
     response = client.get("/materials/usage/999999")
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
     
def test_get_material_usage_success(material_usage):
     _, _, material_id = material_usage
     response = client.get(f"/materials/usage/{material_id}")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     assert json_data
     first_element = json_data[0]
     assert isinstance(first_element, dict)
     assert "MaterialId" in first_element
     
def test_get_top_materials_success(project, material_usage):
     project_id = project
     top_n = "5"
     response = client.get(f"/materials/top/{project_id}/{top_n}")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     assert json_data
     first_element = json_data[0]
     assert isinstance(first_element, dict)
     expected_keys = ["ProjectId", "MaterialTypeName", "MaterialName", "Symbol", "SharePCT"]
     for key in expected_keys:
          assert key in first_element
     assert first_element.get("ProjectId") == project_id
     assert float(first_element["SharePCT"]) == 1.0
     
def test_get_top_materials_invalid_top_n(project):
     project_id = project
     top_n = "0"
     response = client.get(f"/materials/top/{project_id}/{top_n}")
     assert response.status_code == 422
     
def test_get_top_materials_project_not_found():
     top_n = "5"
     response = client.get(f"/materials/top/999999999/{top_n}")
     assert response.status_code == 404
     
def test_add_material_usage_success(element, material_unit, regular_user, db):
     material_id, unit_id = material_unit
     element_id = element
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          f"/materials/usage/{element_id}/{material_id}",
          json={
               "UnitId": unit_id,
               "Quantity": 22
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 201
     json_data = response.json()
     assert isinstance(json_data, dict)
     assert "MaterialUsageId" in json_data
     assert "successfully" in json_data["message"]
     material_usage_id = json_data["MaterialUsageId"]
     try:
          result = db.execute(
               text("""
                         SELECT Quantity FROM MaterialUsage
                         WHERE MaterialUsageId = :material_usage_id;
                    """),
               {"material_usage_id": material_usage_id}
          )
          quantity = result.scalar()
          assert quantity == 22 
     finally:
          db.execute(
               text("""
                    DELETE FROM MaterialUsage
                    WHERE MaterialUsageId = :material_usage_id;
                    """),
               {"material_usage_id": material_usage_id}
          )
          db.commit()

def test_add_material_usage_without_authorization(element, material_unit):
     material_id, unit_id = material_unit
     element_id = element
     response = client.post(
          f"/materials/usage/{element_id}/{material_id}",
          json={
               "UnitId": unit_id,
               "Quantity": 22
          }
     )
     assert response.status_code == 401
   
def test_add_material_usage_invalid_data(element, material_unit, regular_user):
     material_id, unit_id = material_unit
     element_id = element
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          f"/materials/usage/{element_id}/{material_id}",
          json={
               "UnitId": unit_id,
               "Quantity": "invalid"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 422
     
def test_delete_material_usage_success(admin_user, material_usage, db):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     material_usage_id, _, _ = material_usage
     response = client.delete(
          f"/materials/usage/{material_usage_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 204
     result = db.execute(
          text("""
                    SELECT MaterialUsageId FROM MaterialUsage
                    WHERE MaterialUsageId = :material_usage_id
               """),
          {"material_usage_id": material_usage_id}
     )
     obj = result.scalar()
     assert obj is None
     
def test_delete_material_usage_without_authorization(material_usage):
     material_usage_id, _, _ = material_usage
     response = client.delete(
          f"/materials/usage/{material_usage_id}"
     )
     assert response.status_code == 401
     
def test_delete_material_usage_without_admin_role(regular_user, material_usage):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     material_usage_id, _, _ = material_usage
     response = client.delete(
          f"/materials/usage/{material_usage_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 403
     
def test_delete_material_usage_not_found(admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.delete(
          "/materials/usage/99999",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_update_material_usage_not_found(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          "/materials/usage/9999999",
          json={
               "quantity": 91
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_update_material_usage_success(material_usage, regular_user, db):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     material_usage_id, _, _ = material_usage
     response = client.put(
          f"/materials/usage/{material_usage_id}",
          json={
               "quantity": 91
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, dict)
     assert "set" in json_data["message"]
     result = db.execute(
          text("""
                    SELECT Quantity FROM MaterialUsage
                    WHERE MaterialUsageId = :material_usage_id
               """),
          {"material_usage_id": material_usage_id}
     )
     quantity = result.scalar()
     assert quantity == 91

def test_update_material_usage_without_authorization(material_usage):
     material_usage_id, _, _ = material_usage
     response = client.put(
          f"/materials/usage/{material_usage_id}",
          json={
               "quantity": 91
          }
     )
     assert response.status_code == 401