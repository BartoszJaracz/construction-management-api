from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.user import UserResponse, UserMessageResponse, ProjectUserResponse
from app.schemas.exceptions import user_not_found
import logging

logger = logging.getLogger(__name__)


router = APIRouter(
     prefix="/users",
     tags=["Users"]
)

#get all users
@router.get(
     "",
     response_model= list[UserResponse],
     status_code=status.HTTP_200_OK
)
def get_all_users(
     db: Session= Depends(get_db)
):
     result = db.execute(
          text("""
               SELECT * FROM [User] u;
          """)
     )
     
     return [
          row._mapping for row in result.all()
     ]

#get all project users
@router.get(
     "/project",
     response_model=list[ProjectUserResponse],
     status_code=status.HTTP_200_OK
)
def get_all_project_users(
     db: Session= Depends(get_db)
):
     result = db.execute(
          text("""
               SELECT * FROM ProjectUser pu;
          """)
     )
     
     return [
          row._mapping for row in result.all()
     ]
     
#assign user to project
@router.put(
     "/{user_id}/assign_user",
     response_model=UserMessageResponse,
     status_code=status.HTTP_201_CREATED
)
def assign_user_to_project(
     project_id: int,
     user_id: int,
     db: Session= Depends(get_db)
):
     try:
          result = db.execute(
               text("""
                    EXEC sp_AssignUserToProject
                    @ProjectId = :project_id,
                    @UserId = :user_id;
               """),
               {
                    "project_id": project_id,
                    "user_id": user_id
               }
          )
          
     except Exception as e:
          
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot assign user with id {user_id} to project with id {project_id}"
          )
     
     if result.rowcount == 0:
          user_not_found(user_id)
          
     return UserMessageResponse(
          message=f"User with id {user_id} successfully assigned to project with id {project_id}"
     )