from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY ='faca99944566a7d735c52f6665160820713f2c71fccf588aa9103d8a7974d585'
ALGORITHM = "HS256"