from fastapi import APIRouter
from app.models.transfer import TransferCreate
from app.services.transfer_service import TransferService

router = APIRouter()

@router.post("/create", response_model=str)
async def create_transfer(transfer: TransferCreate):
    return await TransferService.create_transfer(transfer)