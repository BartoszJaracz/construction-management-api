from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.element import ElementResponse, ElementMessageResponse, ElementCreate, ElementWithoutCalculationsResponse
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/elements",
     tags=["Elements"]
)

#get top 5 elements
@router.get(
     "",
     response_model=list[ElementResponse]
)
def get_top5_elements(
     db: Session = Depends(get_db)
     ):
     
     result = db.execute(
          text("SELECT TOP 5 * FROM StructuralElement se;")
     )
     
     return [
          row._mapping for row in result
     ]
     
#get element with ElementId
@router.get(
     "/{element_id}",
     response_model=ElementResponse
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
          return {"message": "Project not found"}
     
     return ElementResponse(
          **row._mapping
     )
     
#create new element
@router.post(
     "",
     response_model=ElementMessageResponse
)
def post_element(
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
          
     except Exception as e:
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot create new element"
          )
          
     return ElementMessageResponse(
          message="Element created successfully"
     )
     
#get elements without calculations
@router.get(
     "",
     response_model=ElementWithoutCalculationsResponse
)
def get_elem_without_calcs(
     db: Session = Depends(get_db)
):
     
     result = db.execute(
          text("""SELECT * FROM vw_ElementsWithoutCalculations vewc;""")
     )
     
     return ElementWithoutCalculationsResponse(
          **row._mapping
     )
     
#delete element
@router.delete(
     "/{element_id}",
     status_code=status.HTTP_200_OK
)
def delete_element(
     element_id: int,
     db: Session = Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    DELETE FROM StructuralElement WHERE ElementId = :element_id;
               """),
               {"element_id": element_id}
          )
     
     except Exception as e:
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail= f"Cannot delete Element with ID {element_id}"
          )
     
     if result.rowcount == 0:
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Element with ID {element_id} not found"
          )