from app.config import supabase
from app.models.transfer import TransferCreate

class TransferService:
    @staticmethod
    async def create_transfer(transfer: TransferCreate):
        print("creating transfer")
        pass