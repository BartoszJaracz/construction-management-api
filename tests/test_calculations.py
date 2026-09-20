from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import text
from app.security import create_access_token
from decimal import Decimal

client = TestClient(app)


def test_get_calculations(calculation):
    _, calculation_id = calculation
    response = client.get("/calculations")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    calculation_ids = [
        item["CalculationId"]
        for item in json_data
    ]
    assert calculation_id in calculation_ids

def test_get_calculation(calculation):
     _, calculation_id = calculation
     response = client.get(
          f"/calculations/{calculation_id}"
     )
     assert response.status_code == 200
     json_data = response.json()
     assert json_data["CalculationId"] == calculation_id
     assert json_data["ElementId"] == calculation[0]

def test_get_calculation_not_found():
    response = client.get(
        "/calculations/99999999"
    )
    assert response.status_code == 404
    
def test_create_calculation_success(regular_user, element, db):
     element_id = element
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/calculations",
          json={
               "ElementId": element_id,
               "BendingMoment": 100.00,
               "AxialForce": 75.00,
               "LoadValue": 155.00,
               "LoadCapacityFactor": 0.70
          },
          headers={"Authorization": f"Bearer {token}"}          
     )
     assert response.status_code == 201
     json_data = response.json()
     assert "CalculationId" in json_data
     assert "successfully" in json_data["message"]
     calculation_id = json_data["CalculationId"]
     
     try:
          result = db.execute(
               text("""
                    SELECT * FROM Calculation
                    WHERE ElementId = :element_id
                    AND CalculationId = :calculation_id;     
               """),
               {
                    "element_id": element_id,
                    "calculation_id": calculation_id
               }
          )
          row = result.fetchone()
          assert(
               row.CalculationId == json_data["CalculationId"]
               and row.ElementId == element_id
               and row.BendingMoment == Decimal("100.00")
               and row.AxialForce == Decimal("75.00")
               and row.LoadValue == Decimal("155.00")
               and row.LoadCapacityFactor == Decimal("0.70")
          )
     finally:
          db.execute(
               text("""
                    DELETE FROM Calculation
                    WHERE ElementId = :element_id
                    AND CalculationId = :calculation_id;   
               """),
               {
                    "element_id": element_id,
                    "calculation_id": calculation_id
               }
          )
          db.commit()
     
def test_create_calculation_without_authorization(element):
     element_id = element
     response = client.post(
          "/calculations",
          json={
               "ElementId": element_id,
               "BendingMoment": 100.00,
               "AxialForce": 75.00,
               "LoadValue": 155.00,
               "LoadCapacityFactor": 0.70
          },
     )
     assert response.status_code == 401
     
def test_create_calculation_with_invalid_token(element):
     token = create_access_token(
          data={"sub": "999999999"}
     )
     element_id = element
     response = client.post(
          "/calculations",
          json={
               "ElementId": element_id,
               "BendingMoment": 100.00,
               "AxialForce": 75.00,
               "LoadValue": 155.00,
               "LoadCapacityFactor": 0.70
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 401
     
def test_create_calculation_element_not_found(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.post(
          "/calculations",
          json={
               "ElementId": 9999999,
               "BendingMoment": 100.00,
               "AxialForce": 75.00,
               "LoadValue": 155.00,
               "LoadCapacityFactor": 0.70
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_delete_calculation_without_authorization(calculation):
     _, calculation_id = calculation
     response = client.delete(
          f"/calculations/{calculation_id}"
     )
     assert response.status_code == 401
     
def test_delete_calculation_without_admin_role(calculation, regular_user):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.delete(
          f"/calculations/{calculation_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 403
     
def test_delete_calculation_success(admin_user, calculation, db):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.delete(
          f"/calculations/{calculation_id}",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 204
     result = db.execute(
          text("""
               SELECT CalculationId FROM Calculation
               WHERE CalculationId = :calculation_id     
          """),
          {"calculation_id": calculation_id}
     )
     calcs_id = result.scalar()
     assert calcs_id is None
     
def test_delete_calculation_not_found(admin_user):
     token = create_access_token(
          data={"sub": str(admin_user)}
     )
     response = client.delete(
          "/calculations/9999999999",
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_update_bending_moment_success(calculation, regular_user, db):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          f"/calculations/{calculation_id}/bending_moment",
          json={
               "value": 200.00
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT BendingMoment FROM Calculation
               WHERE CalculationId = :calculation_id     
          """),
          {"calculation_id": calculation_id}
     )
     bending_moment = result.scalar()
     assert bending_moment == Decimal("200.00")
     
def test_update_bending_moment_without_authorization(calculation):
     _, calculation_id = calculation
     response = client.put(
          f"/calculations/{calculation_id}/bending_moment",
          json={
               "value": 200.00
          }
     )
     assert response.status_code == 401
     
def test_update_bending_moment_not_found(regular_user):
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          "/calculations/99999999999/bending_moment",
          json={
               "value": 200.00
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 404
     
def test_update_bending_moment_negative_value(calculation, regular_user):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          f"/calculations/{calculation_id}/bending_moment",
          json={
               "value": -100.00
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 422
     
def test_update_axial_force_success(calculation, regular_user, db):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          f"/calculations/{calculation_id}/axial_force",
          json={
               "value": 100.00
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT AxialForce FROM Calculation
               WHERE CalculationId = :calculation_id     
          """),
          {"calculation_id": calculation_id}
     )
     axial_force = result.scalar()
     assert axial_force == Decimal("100.00")
     
def test_update_load_value_success(calculation, regular_user, db):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          f"/calculations/{calculation_id}/load_value",
          json={
               "value": 150.00
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT LoadValue FROM Calculation
               WHERE CalculationId = :calculation_id     
          """),
          {"calculation_id": calculation_id}
     )
     load_value = result.scalar()
     assert load_value == Decimal("150.00")
     
def test_update_load_capacity_factor_success(calculation, regular_user, db):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          f"/calculations/{calculation_id}/load_capacity_factor",
          json={
               "value": 0.50
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 200
     result = db.execute(
          text("""
               SELECT LoadCapacityFactor FROM Calculation
               WHERE CalculationId = :calculation_id     
          """),
          {"calculation_id": calculation_id}
     )
     load_capacity_factor = result.scalar()
     assert load_capacity_factor == Decimal("0.50")
     
def test_update_load_capacity_factor_zero(calculation, regular_user):
     _, calculation_id = calculation
     token = create_access_token(
          data={"sub": str(regular_user)}
     )
     response = client.put(
          f"/calculations/{calculation_id}/load_capacity_factor",
          json={
               "value": 0
          },
          headers={"Authorization": f"Bearer {token}"}
     )
     assert response.status_code == 422
     