from fastapi.testclient import TestClient
from app.main import app
from app.security import create_access_token
from sqlalchemy import text

client = TestClient(app)



def test_get_projects_success():
     response = client.get("/projects")
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     assert json_data
     first_element = json_data[0]
     assert "ProjectId" in first_element

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
     
def test_get_project_dashboard_success(project):
     project_id = project
     response = client.get(f"/projects/{project_id}/dashboard")
     assert response.status_code == 200
     json_data = response.json()
     assert project_id == json_data["ProjectId"]
     
def test_get_project_dashboard_not_found():
     response = client.get("/projects/999999999/dashboard")
     assert response.status_code == 404

def test_get_project_bottleneck_success(project):
     project_id = project
     response = client.get(f"/projects/{project_id}/bottleneck")
     assert response.status_code == 200
     json_data = response.json()
     assert project_id == json_data["ProjectId"]
     
def test_get_project_bottleneck_not_found():
     response = client.get("/projects/999999999/bottleneck")
     assert response.status_code == 404
     
def test_create_project_invalid_data(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/projects",
          json={
               "DueDate": "not-a-date",              
          },
          headers={
               "Authorization": f"Bearer {token}"
          }
     )
     assert response.status_code == 422
     
def test_create_project_missing_due_date(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/projects",
          json={
               "ProjectName": "Test Project"
          },
          headers={
               "Authorization": f"Bearer {token}"
          }
     )
     assert response.status_code == 422
       
def test_create_project_success(regular_user, db):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/projects",
          json={
               "ProjectName": "Test Project",
               "Scope": "Test Scope",
               "Location": "Test Location",
               "Status": "Nowy",
               "DueDate": "2030-09-30"
          },
          headers={
               "Authorization": f"Bearer {token}"
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
          
def test_create_project_without_authentication():
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
     assert response.status_code == 401
     
def test_create_project_invalid_token():
     token = create_access_token(
          data={"sub": "99999999"}
     )
     response = client.post(
          "/projects",
          json={
               "ProjectName": "Test Project",
               "Scope": "Test Scope",
               "Location": "Test Location",
               "Status": "Nowy",
               "DueDate": "2030-09-30"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 401          
          
def test_update_status_success(regular_user, project, db):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     project_id = project
     response = client.put(
          f"/projects/{project_id}/status",
          json={
               "new_status": "Zakonczony"
          },
          headers={
               "Authorization": f"Bearer {token}"
          }
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT p.Status FROM Project p
               WHERE p.ProjectId = :project_id;   
          """),
          {"project_id": project_id}
     )
     status = result.scalar()
     assert status == "Zakonczony"
     
def test_update_status_without_authentication(project):
     project_id = project
     response = client.put(
          f"/projects/{project_id}/status",
          json={
               "new_status": "Zakonczony"
          }
     )
     assert response.status_code == 401
     
def test_update_status_not_found(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          "/projects/99999999/status",
          json={
               "new_status": "Zakonczony"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_update_status_invalid_status(regular_user, project):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     project_id = project
     response = client.put(
          f"/projects/{project_id}/status",
          json={
               "new_status": "test status"
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 422
     
def test_update_status_missing_status(project, admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     project_id = project
     response = client.put(
          f"/projects/{project_id}/status",
          json={},
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 422
     
def test_delete_project_without_authentication():
     response = client.delete("/projects/1")
     assert response.status_code == 401
     
def test_delete_project_without_admin_role(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.delete(
          "/projects/1",
          headers={
               "Authorization": f"Bearer {token}"
          }
     )
     assert response.status_code == 403
     
def test_delete_project_admin_project_not_found(admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.delete(
          "/projects/99999999",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_delete_project_success(project, admin_user, db):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     project_id = project
     response = client.delete(
          f"/projects/{project_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 204
     query = db.execute(
          text("""
               SELECT ProjectId FROM Project
               WHERE ProjectId = :project_id     
          """),
          {"project_id": project_id}
     )
     result = query.scalar()
     assert result is None