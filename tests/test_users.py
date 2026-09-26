from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import text
from app.security import create_access_token

client = TestClient(app)


def test_get_users_success(admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.get(
          "/users",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     json_data = response.json()
     assert json_data
     assert isinstance(json_data, list)
     assert "UserId" in json_data[0]
          
def test_get_users_without_admin_role(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.get(
          "/users",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 403
     
def test_get_project_users_success(admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.get(
          "/users/project",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     json_data = response.json()
     assert isinstance(json_data, list)
     if json_data:
          assert "UserId" in json_data[0]
          assert "ProjectId" in json_data[0]
          
def test_assign_user_to_project_success(admin_user, regular_user, project, db):
     project_id = project
     user_id = regular_user
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.put(
          f"/users/{user_id}/projects/{project_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT ProjectId
               FROM ProjectUser
               WHERE UserId = :user_id  
          """),
          {"user_id": user_id}
     )
     assigned_project_id = result.scalar()
     assert assigned_project_id == project_id
     db.execute(
          text("""
               DELETE FROM ProjectUser
               WHERE UserId = :user_id
               AND ProjectId = :project_id;     
          """),
          {
               "user_id": user_id,
               "project_id": project_id
          }
     )
     db.commit()
     
def test_register_user_success(db):
     password = "TestPassword1234!"
     email= "TestEmail@test.com"
     response = client.post(
          "/users/register",
          json={
               "first_name": "TestFirstName",
               "last_name": "TestLastName",
               "email": email,
               "password": password               
          }
     )
     assert response.status_code == 201
     result = db.execute(
          text("""
               SELECT * FROM [User]
               WHERE Email = :email;
          """),
          {"email": email}
     )
     new_user = result.fetchone()
     assert new_user is not None
     assert new_user["Role"] == "ASYSTENT"
     assert new_user["IsActive"] == 1
     assert new_user["PasswordHash"] != password
     db.execute(
          text("""
               DELETE FROM [User]
               WHERE Email = :email;     
          """),
          {"email": email}
     )
     db.commit()
     
def test_register_user_email_already_exists(login_user):
     _, email, _ = login_user
     response = client.post(
          "/users/register",
          json={
               "first_name": "TestFirstName",
               "last_name": "TestLastName",
               "email": email,
               "password": "TestPassword1234!"               
          }
     )
     assert response.status_code == 409
     