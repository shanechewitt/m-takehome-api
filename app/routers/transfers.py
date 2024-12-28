from fastapi import APIRouter
from app.models.transfer import TransferCreate, Transfer
from app.services.transfer_service import TransferService

router = APIRouter()

@router.post("/create-transfer", response_model=Transfer)
async def create_transfer(transfer: TransferCreate):
    return await TransferService.create_transfer(transfer)