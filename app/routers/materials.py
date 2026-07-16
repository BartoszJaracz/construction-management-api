from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from app.database import get_db
from app.schemas.material import MaterialResponse, MaterialUsageResponse, TopMaterialPerProjectResponse, MaterialUsageAdd, MaterialMessageResponse
from app.schemas.exceptions import material_not_found, project_not_found, element_not_found, material_usage_not_found
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/materials",
     tags=["Materials"]
)

#get all materials
@router.get(
     "",
     status_code=status.HTTP_200_OK,
     response_model=list[MaterialResponse]
)
def get_materials(
     db: Session= Depends(get_db)  
):
     result = db.execute(
          text("""
               SELECT * FROM Material m;
          """)
     )
     
     return [
          row._mapping for row in result.all()
     ]

#get material usage by MaterialId
@router.get(
     "/usage/{material_id}",
     status_code=status.HTTP_200_OK,
     response_model=list[MaterialUsageResponse]
)
def get_material_usage_with_material_id(
     material_id: int,
     db: Session= Depends(get_db)
):
     result = db.execute(
          text("""
               SELECT * FROM MaterialUsage mu
               WHERE mu.MaterialId = :material_id;
          """),
          {"material_id": material_id}
     )
     
     rows= result.fetchall()
     
     if not rows:
          material_not_found(material_id)
     
     return [MaterialUsageResponse(**row._mapping) for row in rows]

#add material usage by ElementId & MaterialId
@router.post(
     "/usage/{element_id}/{material_id}",
     status_code=status.HTTP_201_CREATED,
     response_model=MaterialMessageResponse
)
def add_material_usage(
     element_id: int,
     material_id: int,
     material_usage: MaterialUsageAdd,
     db: Session= Depends(get_db)
):
     try:
          #combine all parameteres into one
          query_params = material_usage.model_dump()
          query_params.update({
               "ElementId": element_id,
               "MaterialId": material_id
          })
          
          db.execute(
               text("""
                    INSERT INTO MaterialUsage
                    (
                         ElementId,
                         MaterialId,
                         UnitId,
                         Quantity,
                         UsedAt
                    )
                    VALUES
                    (
                         :ElementId,
                         :MaterialId,
                         :UnitId,
                         :Quantity,
                         GETDATE()
                    )
               """),
               query_params
          )
          
     except Exception as e:
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot add material usage"
          )
          
     return MaterialMessageResponse(
          message="Material usage added successfully"
     )

#delete MaterialUsage by ElementId & Quantity
@router.delete(
     "/usage/{element_id}/{quantity}",
     status_code=status.HTTP_204_NO_CONTENT
)
def delete_material_usage(
     element_id: int,
     quantity: Decimal,
     db: Session= Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    DELETE FROM MaterialUsage
                    WHERE ElementId = :element_id
                    AND Quantity = :quantity;
               """),
               {
                    "element_id": element_id,
                    "quantity": quantity
               }
          )
     except Exception as e:
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot delete MaterialUsage with ElementId {element_id} and Quantity {quantity}"
          )
          
     if result.rowcount == 0:
          element_not_found(element_id)          

#update MaterialUsage by ElementId & Quantity
@router.put(
     "/usage/{element_id}/{quantity}/{new_quantity}",
     response_model= MaterialMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def update_material_usage_quantity(
     element_id: int,
     quantity: Decimal,
     new_quantity: Decimal,
     db: Session= Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    UPDATE MaterialUsage
                    SET Quantity = :new_quantity
                    WHERE ElementId = :element_id
                    AND quantity = :quantity; 
               """),
               {
                    "element_id": element_id,
                    "quantity": quantity,
                    "new_quantity": new_quantity
               }
          )
          
          if result.rowcount==0:
               material_usage_not_found(element_id, quantity)
          
     except Exception as e:
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot update material usage quantity with ElementId {element_id}"
          )

     return MaterialMessageResponse(
          message=f"Quantity {new_quantity} set to element with ID {element_id}"
     )

#get top material per project
@router.get(
     "/{project_id}/{top_n}",
     status_code=status.HTTP_200_OK,
     response_model=list[TopMaterialPerProjectResponse]
)
def get_top_material_per_project(
     project_id: int,
     top_n: int,
     db: Session= Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    EXEC sp_GetTopMaterialPerProject
                    @ProjectId = :project_id,
                    @TopN = :top_n;
               """),
               {
                    "project_id": project_id,
                    "top_n": top_n
               }
          )
          
          rows = result.fetchall()
          
          if not rows:
               project_not_found(project_id)
          
          return [
               TopMaterialPerProjectResponse(**row._mapping) for row in rows
          ]
          
#error handle in python
     except DBAPIError:
          project_not_found(project_id)