from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.element import ElementResponse, ElementCreate, ElementWithoutCalculationsResponse
from app.schemas.calculation import CalculationResponse
from app.schemas.exceptions import element_not_found, latest_calculation_not_found
from app.schemas.common import MessageResponse
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/elements",
     tags=["Elements"]
)

#get top 5 elements
@router.get(
     "",
     response_model=list[ElementResponse],
     status_code=status.HTTP_200_OK
)
def get_top5_elements(
     db: Session = Depends(get_db)
     ):
     
     result = db.execute(
          text(""""SELECT TOP 5 *
               FROM StructuralElement se
               ORDER BY se.CreatedAt;""")
     )
     
     return [
          row._mapping for row in result.all()
     ]
     
#get elements without calculations
@router.get(
     "/without-calcs",
     response_model=list[ElementWithoutCalculationsResponse],
     status_code=status.HTTP_200_OK
)
def get_elements_without_calculations(
     db: Session = Depends(get_db)
):
     
     result = db.execute(
          text("""SELECT * FROM vw_ElementsWithoutCalculations vewc;""")
     )
     
     return [
          row._mapping for row in result.all()
     ]
          
#get element with ElementId
@router.get(
     "/{element_id}",
     response_model=ElementResponse,
     status_code=status.HTTP_200_OK
)
def get_element(
     element_id: int,
     db: Session = Depends(get_db)
     ):
     
     result = db.execute(
          text("""
               SELECT * FROM StructuralElement se
               WHERE se.ElementId = :element_id;
          """),
          {"element_id": element_id}
     )
     
     row = result.fetchone()
     
     if row is None:
          element_not_found(element_id) 
     
     return ElementResponse(
          **row._mapping
     )

#get LATEST calculations with ElementId
@router.get(
     "/{element_id}/calculations/latest",
     status_code=status.HTTP_200_OK,
     response_model=CalculationResponse
)
def get_latest_calculation(
     element_id: int,
     db: Session= Depends(get_db)
):
     result = db.execute(
          text("""
               SELECT * FROM vw_LatestCalculationsPerElement vlcpe
               WHERE vlcpe.ElementId = :element_id AND vlcpe.isLatest = 1;    
          """),
          {"element_id": element_id}
     )
     
     row = result.fetchone()
     
     if row is None:
          latest_calculation_not_found(element_id)
     
     return CalculationResponse(
          **row._mapping
     )

#create new element
@router.post(
     "",
     response_model=MessageResponse,
     status_code=status.HTTP_201_CREATED
)
def create_element(
     element: ElementCreate,
     db: Session = Depends(get_db)
):
     try:
          db.execute(
               text("""
                    EXEC sp_AddStructuralElement
                         @ProjectId = :ProjectId,
                         @ElementTypeId = :ElementTypeId,
                         @Name = :Name,
                         @Dimensions = :Dimensions,
                         @TechnicalParameters = :TechnicalParameters;
               """),
               element.model_dump()
          )
          
          db.commit()
          
     except Exception:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot create new element"
          )
          
     return MessageResponse(
          message="Element created successfully"
     )
        
#delete element
@router.delete(
     "/{element_id}",
     status_code=status.HTTP_204_NO_CONTENT
)
def delete_element(
     element_id: int,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    DELETE FROM StructuralElement
                    WHERE ElementId = :element_id;
               """),
               {"element_id": element_id}
          )
           
          db.commit()
     
     except Exception:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail= f"Cannot delete Element with ID {element_id}"
          )
          
     if result.rowcount == 0:
          element_not_found(element_id)
          
     
#update element dimensions
@router.put(
     "/dimensions/{element_id}",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
)
def update_element_dimensions(
     element_id: int,
     new_dimensions: str,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    UPDATE StructuralElement
                    SET Dimensions = :new_dimensions
                    WHERE ElementId = :element_id
               """),
               {
                    "element_id": element_id,
                    "new_dimensions": new_dimensions
               }
          )
               
          db.commit()
               
     except Exception:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot update element with ID {element_id}"
          )
     
     if result.rowcount == 0:
          element_not_found(element_id)
     
     return MessageResponse(
          message=f"Element with ID {element_id} set new element dimensions: {new_dimensions}"
     )