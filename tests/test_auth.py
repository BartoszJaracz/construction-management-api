from fastapi.testclient import TestClient
from app.main import app



client = TestClient(app)

def test_login_wrong_password():
     response = client.post(
          "/auth/login",
          data={
               "username": "pytest@test.com",
               "password": "WrongPassword123!"
          }
     )
     
     assert response.status_code == 401
     
def test_login_success():
     response = client.post(
          "/auth/login",
          data={
               "username": "pytest@test.com",
               "password": "TestPassword123!"
          }
     )
     
     assert response.status_code == 200
     
     json_data = response.json()
     
     assert "access_token" in json_data
     assert json_data["token_type"] == "bearer"