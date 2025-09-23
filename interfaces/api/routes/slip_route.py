from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.db.connection import get_db
from application.usecases.slip_services import SlipService
from schemas.slip_schema import SlipCreate, SlipUpdate, SlipResponse
from application.usecases.user_services import UserService
from application.usecases.helper.get_current_user_service import get_current_user_service
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
oauth2_scheme = HTTPBearer()

# async def get_current_user_id(
#     credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db)
# ):
#     user_service = UserService()
#     user = await user_service.get_current_user(credentials, db)
#     return user.id

@router.post("/", response_model=SlipResponse, status_code=status.HTTP_201_CREATED)
async def create_slip(data: SlipCreate, db: AsyncSession = Depends(get_db), current_user= Depends(get_current_user_service)):
    return await SlipService(db).create_slip(data, current_user.id)

@router.get("/{slip_id}", response_model=SlipResponse)
async def get_slip(slip_id: int, db: AsyncSession = Depends(get_db), current_user= Depends(get_current_user_service)):
    return await SlipService(db).get_slip(slip_id, current_user.id)

@router.get("/", response_model=list[SlipResponse])
async def get_user_slips(db: AsyncSession = Depends(get_db),current_user = Depends(get_current_user_service)):
    return await SlipService(db).get_user_slips(current_user.id)

@router.put("/{slip_id}", response_model=SlipResponse)
async def update_slip(slip_id: int, data: SlipUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user_service)):
    return await SlipService(db).update_slip(slip_id, data, current_user.id)

@router.delete("/{slip_id}")
async def delete_slip(slip_id: int, db: AsyncSession = Depends(get_db), current_user= Depends(get_current_user_service)):
    return await SlipService(db).delete_slip(slip_id, current_user.id)
