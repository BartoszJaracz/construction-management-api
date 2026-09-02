#httpException
from fastapi import HTTPException, status
from decimal import Decimal


#project not found exception
def project_not_found(project_id: int):
     raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Project with ID {project_id} not found"
     )
     
#element not found exception
def element_not_found(element_id: int):
     raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Element with ID {element_id} not found"
     )
     
#calculation not found exception
def calculation_not_found(calculation_id: int):
     raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Calculation with ID {calculation_id} not found"
     )

#calculation update exception
def calculation_update_exception(calculation_id: int):
     raise HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Cannot update calculation with ID {calculation_id}"
     )
     
#material not found exception
def material_not_found(material_id: int):
     raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"Material with ID {material_id} not found"
     )
     
#material-usage not found exception
def material_usage_not_found(
     material_usage_id: int
     ):
          raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail=f"Material usage with ID {material_usage_id} not found"
          )
          
#user not found exception
def user_not_found(user_id: int):
     raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail=f"User with ID {user_id} not found"
     )

#latest calcs not found exception 
def latest_calculation_not_found(element_id: int):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Latest calculation for element with ID {element_id} not found"
    )