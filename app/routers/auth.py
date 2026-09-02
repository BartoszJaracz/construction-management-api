from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.schemas.user import TokenResponse
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
     form_data: OAuth2PasswordRequestForm = Depends(),
     db: Session= Depends(get_db)
) -> TokenResponse:
     #login exception
     login_exception = HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Invalid email or password"
          )
       
     result = db.execute(
          text("""
               SELECT u.UserId, u.PasswordHash FROM [User] u
               WHERE u.Email = :email;
          """),
          {"email": form_data.username}
     )
          
     user = result.fetchone()
          
     if not user:
          raise login_exception
       
     if not verify_password(form_data.password, user.PasswordHash):
          raise login_exception
          
     try:               
          db.execute(
               text("""
                    UPDATE [User]
                    SET LastLogin = GETDATE()
                    WHERE UserId = :user_id;
               """),
               {"user_id": user.UserId}
          )
          db.commit()
          
     except Exception:
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
          
          
     