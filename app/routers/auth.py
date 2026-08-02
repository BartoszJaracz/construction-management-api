from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.user import UserLogin, TokenResponse
from app.security import verify_password, create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
     prefix="/auth",
     tags=["Authentication"]
)

#user login
@router.post(
     "/login",
     response_model=TokenResponse,
     status_code=status.HTTP_200_OK
)
def user_login(
     payload: UserLogin,
     db: Session= Depends(get_db)
):

     result = db.execute(
          text("""
               SELECT u.UserId, u.PasswordHash FROM [User] u
               WHERE u.Email = :email;
          """),
          {"email": payload.email}
     )
          
     user = result.fetchone()
          
     if user is None:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid email or password"
          )
               
     if not verify_password(payload.password, user.PasswordHash):
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid email or password"
          )
          
     try:               
          db.execute(
               text("""
                    UPDATE [User] u
                    SET u.LastLogin = GETDATE()
                    WHERE u.UserId = :user_id;
               """),
               {"user_id": user.UserId}
          )
          db.commit()
          
     except Exception as e:
          db.rollback()
          
          logger.exception("Database error")
          
          raise HTTPException(
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
               detail="Login failed"
          )
          
     access_token = create_access_token(
          data={
               "sub": str(user.UserId)
          }
     )
          
     return TokenResponse(
          access_token=access_token,
          token_type="bearer"
     )
          
          
     