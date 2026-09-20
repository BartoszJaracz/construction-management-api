from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy import text
from app.database import get_db
from app.schemas.calculation import(
          CalculationResponse,
          CalculationCreate,
          CalculationMessageResponse,
          CalculationNonNegativeUpdate,
          CalculationPositiveUpdate
     )
from app.schemas.common import MessageResponse
from app.schemas.exceptions import(
          calculation_not_found,
          calculation_update_exception,
          database_error,
          element_not_found
     )
from app.dependencies import get_current_user, require_admin
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
) -> list[CalculationResponse]:
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
     calculation_id: int,
     db: Session= Depends(get_db)
) -> CalculationResponse:
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
     current_user = Depends(get_current_user),
     db: Session= Depends(get_db)
) -> CalculationMessageResponse:
     try:
          result = db.execute(
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
          calculation_id = result.scalar()
          db.commit()
          
     except ProgrammingError as e:
          db.rollback()
          if "50001" in str(e):
               element_not_found(calculation.ElementId)
          logger.exception("Database error")
          database_error("Cannot create new calculation")
          
     except Exception:
          db.rollback()
          logger.exception("Database error")
          database_error("Cannot create new calculation")
                    
     return CalculationMessageResponse(
          CalculationId=calculation_id,
          message="Calculation created successfully"
     )
     
#delete calculation
@router.delete(
     "/{calculation_id}",
     status_code=status.HTTP_204_NO_CONTENT
)
def delete_calculation(
     calculation_id: int,
     current_user = Depends(require_admin),
     db: Session= Depends(get_db)
) -> None:
     try:
          result = db.execute(
               text("""
                    DELETE FROM Calculation
                    WHERE CalculationId = :calculation_id;
               """),
               {"calculation_id": calculation_id}
          )
          
          db.commit()
          
     except Exception:
          db.rollback()
          logger.exception("Database error")
          database_error(f"Cannot delete calculation with ID {calculation_id}")
          
     if result.rowcount == 0:
          calculation_not_found(calculation_id)
     
          
#update bending moment
@router.put(
     "/{calculation_id}/bending_moment",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
)
def update_bending_moment(
     calculation_id: int,
     bending_moment: CalculationNonNegativeUpdate,
     current_user = Depends(get_current_user),
     db: Session = Depends(get_db)
) -> MessageResponse:
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET BendingMoment = :bending_moment
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "bending_moment": bending_moment.value
               }
          )
          
          db.commit()     
          
     except IntegrityError:
          db.rollback()
          logger.exception("Integrity error while updating bending moment")
          calculation_update_exception(calculation_id)
          
     except Exception:
          db.rollback()
          logger.exception("Database error while updating bending moment")
          calculation_update_exception(calculation_id)
     
     if result.rowcount == 0:
          calculation_not_found(calculation_id)
          
     return MessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated bending moment to {bending_moment.value}"
     )
     
#update axial force
@router.put(
     "/{calculation_id}/axial_force",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
)
def update_axial_force(
     calculation_id: int,
     axial_force: CalculationNonNegativeUpdate,
     current_user = Depends(get_current_user),
     db: Session = Depends(get_db)
) -> MessageResponse:
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET AxialForce = :axial_force
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "axial_force": axial_force.value
               }
          )
               
          db.commit()
          
     except IntegrityError:
          db.rollback()
          logger.exception("Integrity error while updating axial force")
          calculation_update_exception(calculation_id)
               
     except Exception:
          db.rollback()
          logger.exception("Database error while updating axial force")
          calculation_update_exception(calculation_id)
     
     if result.rowcount == 0:
          calculation_not_found(calculation_id)
          
     return MessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated axial force to {axial_force.value}"
     )
     
#update load value
@router.put(
     "/{calculation_id}/load_value",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
)
def update_load_value(
     calculation_id: int,
     load_value: CalculationNonNegativeUpdate,
     current_user = Depends(get_current_user),
     db: Session = Depends(get_db)
) -> MessageResponse:
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET LoadValue = :load_value
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "load_value": load_value.value
               }
          )
               
          db.commit()
     
     except IntegrityError:
          db.rollback()
          logger.exception("Integrity error while updating load value")
          calculation_update_exception(calculation_id)
               
     except Exception:
          db.rollback()
          logger.exception("Database error while updating load value")
          calculation_update_exception(calculation_id)
     
     if result.rowcount == 0:
          calculation_not_found(calculation_id)
          
     return MessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated load value to {load_value.value}"
     )
     
#update load capacity factor
@router.put(
     "/{calculation_id}/load_capacity_factor",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
)
def update_load_capacity_factor(
     calculation_id: int,
     load_capacity_factor: CalculationPositiveUpdate,
     current_user = Depends(get_current_user),
     db: Session = Depends(get_db)
) -> MessageResponse:
     try:
          result = db.execute(
               text("""
                    UPDATE Calculation
                    SET LoadCapacityFactor = :load_capacity_factor
                    WHERE CalculationId = :calculation_id;
               """),
               {
                    "calculation_id": calculation_id,
                    "load_capacity_factor": load_capacity_factor.value
               }
          )
            
          db.commit()
          
     except IntegrityError:
          db.rollback()
          logger.exception("Integrity error while updating load capacity factor")
          calculation_update_exception(calculation_id)
               
     except Exception:
          db.rollback()
          logger.exception("Database error while updating load capacity factor")
          calculation_update_exception(calculation_id)
          
     if result.rowcount == 0:
          calculation_not_found(calculation_id)
     
     return MessageResponse(
          message=f"Calculation with ID {calculation_id} successfully updated load capacity factor to {load_capacity_factor.value}"
     )