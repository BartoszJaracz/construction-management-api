from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import text

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
          
def test_create_element_success(db):
     response = client.post(
          "/elements",
          json={
               "ProjectId": 1,
               "ElementTypeId": 1,
               "Name": "Test element",
               "Dimensions": "100x100",
               "TechnicalParameters": "Test parameters"
          }
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
     