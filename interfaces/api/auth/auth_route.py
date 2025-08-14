import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.db.connection import get_db
from schemas.user_schema import UserCreate, UserLogin, UserResponse
from application.usecases.user_services import UserService
from infrastructure.db.repositories.user_repo_impl import UserRepositoryImpl

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(data: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return await service.register(data)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Cetak traceback lengkap ke console
        error_trace = traceback.format_exc()
        logger.error(f"Unexpected error: {e}\n{error_trace}")

        # Kirim pesan error yang lebih jelas ke response
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db )):
    service = UserService(UserRepositoryImpl(db))
    token = service.login(user.email, user.password)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return token

