from fastapi.testclient import TestClient
from app.main import app
from tests.conftest import db

client = TestClient(app)


def test_get_elements(db):
     response = client.get("/elements")
     
     assert response.status_code == 200
     
     json_data = response.json()
     
     assert isinstance(json_data, list)
     if json_data:
          assert "ElementId" in json_data[0]
          
def test_get_element_success():
     response = client.get("/elements/1")
     
     assert response.status_code == 200
     
     json_data = response.json()
     
     assert isinstance(json_data, dict)
     assert "ElementId" in json_data
     assert json_data["ElementId"] == 1
     
def test_get_element_not_found():
     response = client.get("/elements/9999999")
     
     assert response.status_code == 404
     
     json_data = response.json()
     assert "not found" in json_data["detail"]
     
def test_get_elements_without_calculations():
     response = client.get("/elements/without-calcs")
     
     assert response.status_code == 200
     
     json_data = response.json()
     
     assert isinstance(json_data, list)
     if json_data:
          first_element = json_data[0]
          assert isinstance(first_element, dict)
          assert "ProjectId" in first_element