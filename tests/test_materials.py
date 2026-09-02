from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import db, material_usage
from sqlalchemy import text

client = TestClient(app)


def test_get_material_usage_not_found():
     response = client.get("/materials/usage/999999")
     
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
     
def test_get_material_usage_success():
     response = client.get("/materials/usage/1")
     
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     assert json_data
     
     first_element = json_data[0]
     
     assert isinstance(first_element, dict)
     assert "MaterialId" in first_element
     
def test_add_material_usage_success(db):
     response = client.post(
          "/materials/usage/2/2",
          json={
               "UnitId": 2,
               "Quantity": 22
          }
     )
     
     assert response.status_code == 201
     json_data = response.json()
     assert isinstance(json_data, dict)
     assert "successfully" in json_data["message"]
     
def test_add_material_usage_invalid_data():
     response = client.post(
          "/materials/usage/2/2",
          json={
               "UnitId": 2,
               "Quantity": "invalid"
          }
     )
     
     assert response.status_code == 422
     
def test_delete_material_usage_success(material_usage, db):
     response = client.delete(f"/materials/usage/{material_usage}")
     assert response.status_code == 204
     
     result = db.execute(
          text("""
                    SELECT MaterialUsageId FROM MaterialUsage
                    WHERE MaterialUsageId = :material_usage_id
               """),
          {"material_usage_id": material_usage}
     )
     obj = result.scalar()
     
     assert obj is None
     
def test_delete_material_usage_not_found():
     response = client.delete("/materials/usage/99999")
     
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_update_material_usage_not_found():
     response = client.put(
          "/materials/usage/9999999/91"
     )
     
     assert response.status_code == 404
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_update_material_usage_success(material_usage, db):
     response = client.put(
          f"/materials/usage/{material_usage}/91"
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
          {"material_usage_id": material_usage}
     )
     quantity = result.scalar()
     
     assert quantity == 91