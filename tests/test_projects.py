from fastapi.testclient import TestClient
from app.main import app
from app.security import create_access_token

client = TestClient(app)

def test_get_project_success():
     response = client.get("/projects/1")
     
     assert response.status_code == 200
     
     json_data = response.json()
     
     assert "ProjectId" in json_data
     assert json_data["ProjectId"] == 1
     
def test_get_project_not_found():
     response = client.get("/projects/99999")
     
     assert response.status_code == 404
     
def test_create_project_invalid_data():
     response = client.post(
          "/projects",
          json={
               "DueDate": "not-a-date",              
          }
     )
     
     assert response.status_code == 422
     
def test_create_project_missing_due_date():
     response = client.post(
          "/projects",
          json={
               "ProjectName": "Test Project"
          }
     )
     
     assert response.status_code == 422
     
def test_delete_project_without_authentication():
     response = client.delete("/projects/1")
     
     assert response.status_code == 401
     
def test_delete_project_without_admin_role():
     token = create_access_token(
          data={"sub": "1004"}
     )
     
     response = client.delete(
          "/projects/1",
          headers={
               "Authorization": f"Bearer {token}"
          }
     )
     
     assert response.status_code == 403
     
