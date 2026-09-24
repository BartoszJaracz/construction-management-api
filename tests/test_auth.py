from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app



client = TestClient(app)

def test_login_wrong_password(login_user):
     _, email, _ = login_user
     response = client.post(
          "/auth/login",
          data={
               "username": email,
               "password": "WrongPassword123!"
          }
     )
     assert response.status_code == 401
     
def test_login_success(login_user):
     _, email, password = login_user
     response = client.post(
          "/auth/login",
          data={
               "username": email,
               "password": password
          }
     )
     assert response.status_code == 200
     json_data = response.json()
     assert "access_token" in json_data
     assert json_data["token_type"] == "bearer"
     
def test_login_user_not_found():
     response = client.post(
          "/auth/login",
          data={
               "username": "doesnotexist@test.com",
               "password": "TestPassword123!"
          }
     )
     assert response.status_code == 401

def test_login_updates_last_login(login_user, db):
     user_id, email, password = login_user
     response = client.post(
          "/auth/login",
          data={
               "username": email,
               "password": password
          }
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT LastLogin
               FROM [User]
               WHERE UserId = :user_id     
          """),
          {"user_id": user_id}
     )
     last_login = result.scalar()
     assert last_login is not None