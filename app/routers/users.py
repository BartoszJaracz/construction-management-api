from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.user import(
          UserResponse,
          ProjectUserResponse,
          UserRegister
     )
from app.schemas.common import MessageResponse
from app.security import get_password_hash
from app.dependencies import require_admin
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
     current_user = Depends(require_admin),
     db: Session= Depends(get_db)
) -> list[UserResponse]:
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
     current_user = Depends(require_admin),
     db: Session= Depends(get_db)
) -> list[ProjectUserResponse]:
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
     "/{user_id}/projects/{project_id}",
     response_model=MessageResponse,
     status_code=status.HTTP_200_OK
)
def assign_user_to_project(
     project_id: int,
     user_id: int,
     current_user = Depends(require_admin),
     db: Session= Depends(get_db)
) -> MessageResponse:
     try:
          db.execute(
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
               
          db.commit()
          
     except Exception:
          db.rollback()
          logger.exception("Database error")
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail=f"Cannot assign user with id {user_id} to project with id {project_id}"
          )
     
     return MessageResponse(
          message=f"User with id {user_id} successfully assigned to project with id {project_id}"
     )
     
#user register
@router.post(
     "/register",
     response_model=MessageResponse,
     status_code=status.HTTP_201_CREATED
)
def register(
     user_data: UserRegister,
     db: Session= Depends(get_db)
) -> MessageResponse:
     result = db.execute(
          text("""
               SELECT u.UserId FROM [User] u WHERE u.Email = :email;
          """),
          {"email": user_data.email}
     )
     
     existing_user = result.fetchone()
     
     if existing_user is not None:
          raise HTTPException(
               status_code=status.HTTP_409_CONFLICT,
               detail=f"User with given email - {user_data.email} - already exists."
          )
     hashed_password = get_password_hash(user_data.password)
     
     query_params = {
          "FirstName": user_data.first_name,
          "LastName": user_data.last_name,
          "Email": user_data.email,
          "PasswordHash": hashed_password
     }
     try:
          db.execute(
               text("""
                    INSERT INTO [User]
                    (
                    FirstName,
                    LastName,
                    Email,
                    Role,
                    IsActive,
                    CreatedAt,
                    PasswordHash
                    )
                    VALUES
                    (
                    :FirstName,
                    :LastName,
                    :Email,
                    'ASYSTENT',
                    1,
                    GETDATE(),
                    :PasswordHash
                    )
               """),
               query_params
          )
          
          db.commit()
     
     except Exception:
          db.rollback()
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Cannot register user"
          )
     
     
     return MessageResponse(
          message=f"User with email: {user_data.email} registered successfully."
     )
     