from fastapi.testclient import TestClient
from app.main import app
from app.security import create_access_token
from sqlalchemy import text

client = TestClient(app)

def test_get_project_success(project):
     project_id = project
     response = client.get(f"/projects/{project_id}")
     
     assert response.status_code == 200
     json_data = response.json()
     assert "ProjectId" in json_data
     assert json_data["ProjectId"] == project_id
     
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
     
def test_create_project_success(db):
     response = client.post(
          "/projects",
          json={
               "ProjectName": "Test Project",
               "Scope": "Test Scope",
               "Location": "Test Location",
               "Status": "Nowy",
               "DueDate": "2030-09-30"
          }
     )
     assert response.status_code == 201
     json_data = response.json()
     assert isinstance(json_data, dict)
     assert "ProjectId" in json_data
     assert "successfully" in json_data["message"]
     project_id = json_data["ProjectId"]
     
     try:
          result = db.execute(
               text("""
                    SELECT ProjectName FROM Project
                    WHERE ProjectId = :project_id;
               """),
               {"project_id": project_id}
          )
          name = result.scalar()
          assert name == "Test Project"
     finally:
          db.execute(
               text("""
                    DELETE FROM Project
                    WHERE ProjectId = :project_id
               """),
               {"project_id": project_id}
          )
          db.commit()