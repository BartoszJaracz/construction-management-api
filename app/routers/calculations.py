from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.calculation import CalculationResponse, CalculationCreate, CalculationMessageResponse
from app.schemas.exceptions import calculation_not_found, calculation_update_exception
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/calculations",
     tags=["Calculations"]
)

#get all calculations
@router.get(
     "",
     response_model=list[CalculationResponse],
     status_code=status.HTTP_200_OK
)
def get_all_calculations(
     db: Session= Depends(get_db)
):
     result = db.execute(
          text("""
               SELECT * FROM Calculation c;
          """)
     )
     
     return [
          row._mapping for row in result.all()
     ]
     
#get calculations with CalculationId
@router.get(
     "/{calculation_id}",
     response_model=CalculationResponse,
     status_code=status.HTTP_200_OK
)
def get_calculation(
     calculation_id = int,
     db: Session= Depends(get_db)
):
     result = db.execute(
          text("""
               SELECT * FROM Calculation c
               WHERE c.CalculationId = :calculation_id;
          """),
          {"calculation_id": calculation_id}
     )
     
     row = result.fetchone()
     
     if row is None:
          calculation_not_found(calculation_id)
     
     return CalculationResponse(
          **row._mapping
     )

#add calculation
@router.post(
     "",
     response_model=CalculationMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def create_calculation(
     calculation: CalculationCreate,
     db: Session= Depends(get_db)
):
     try:
          db.execute(
               text("""
                    EXEC sp_AddCalculations
                    @ElementId = :ElementId,
                    @BendingMoment = :BendingMoment,
                    @AxialForce = :AxialForce,
                    @LoadValue = :LoadValue,
                    @LoadCapacityFactor = :LoadCapacityFactor;
               """),
               calculation.model_dump()
          )
          
          db.commit()
          
     except Exception as e:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot create new calculation"
          )
          
     return CalculationMessageResponse(
          message="Calculation created successfully"
     )
     
#delete calculation
@router.delete(
     "/{calculation_id}",
     status_code=status.HTTP_204_NO_CONTENT
)
def delete_calculation(
     calculation_id: int,
     db: Session= Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    DELETE FROM Calculation
                    WHERE CalculationId = :calculation_id;
               """),
               {"calculation_id": calculation_id}
          )
          
          if result.rowcount == 0:
               db.rollback()
               calculation_not_found(calculation_id)
          
          db.commit()
          
     except Exception as e:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot delete calculation with ID {calculation_id}"
          )
     
     
          
#update bending moment
@router.put(
     "/{calculation_id}/bending_moment",
     response_model=CalculationMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def update_bending_moment(
     calculation_id: int,
     bending_moment: Decimal,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET BendingMoment = :bending_moment
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "bending_moment": bending_moment
               }
          )
          
          if result.rowcount == 0:
               db.rollback()
               calculation_not_found(calculation_id)
          
          db.commit()     
          
     except Exception as e:
          db.rollback()
          logger.exception("Database error")
          return calculation_update_exception(calculation_id)
          
     return CalculationMessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated bending moment to {bending_moment}"
     )
     
#update axial force
@router.put(
     "/{calculation_id}/axial_force",
     response_model=CalculationMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def update_axial_force(
     calculation_id: int,
     axial_force: Decimal,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET AxialForce = :axial_force
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "axial_force": axial_force
               }
          )
          
          if result.rowcount == 0:
               db.rollback()
               calculation_not_found(calculation_id)
               
          db.commit()
          
     except Exception as e:
          db.rollback()
          logger.exception("Database error")
          return calculation_update_exception(calculation_id)
          
     return CalculationMessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated axial force to {axial_force}"
     )
     
#update load value
@router.put(
     "/{calculation_id}/load_value",
     response_model=CalculationMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def update_load_value(
     calculation_id: int,
     load_value: Decimal,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET LoadValue = :load_value
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "load_value": load_value
               }
          )
          
          if result.rowcount == 0:
               db.rollback()
               calculation_not_found(calculation_id)
               
          db.commit()
     
     except Exception as e:
          db.rollback()
          logger.exception("Database error")
          return calculation_update_exception(calculation_id)
          
     return CalculationMessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated load value to {load_value}"
     )
     
#update load capacity factor
@router.put(
     "/{calculation_id}/load_capacity_factor",
     response_model=CalculationMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def update_load_capacity_factor(
     calculation_id: int,
     load_capacity_factor: Decimal,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET LoadCapacityFactor = :load_capacity_factor
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "load_capacity_factor": load_capacity_factor
               }
          )
          
          if result.rowcount == 0:
               db.rollback()
               calculation_not_found(calculation_id)
               
          db.commit()
          
     except Exception as e:
          db.rollback()
          logger.exception("Database error")
          return calculation_update_exception(calculation_id)
          
     return CalculationMessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated load capacity factor to {load_capacity_factor}"
     )