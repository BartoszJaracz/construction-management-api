from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import SECRET_KEY, ALGORITHM
import logging


logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
     
     login_exception = HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Could not validate credentials",
          headers={
               "WWW-Authenticate": "Bearer"
          }
     )
     
     
     #decode token:
     try:
          payload = jwt.decode(
               token,
               SECRET_KEY,
               algorithms=[ALGORITHM]
          )
          
          user_id = payload.get("sub")
          
          if not user_id:
               raise login_exception
     
     except JWTError as e:
          logger.warning(e)
          
          raise login_exception
     
     result = db.execute(
          text("""
               SELECT * FROM [User] u WHERE u.UserId = :user_id;
          """),
          {"user_id": user_id}
     )
     
     user = result.fetchone()
     
     if not user:
          raise login_exception
     
     return user