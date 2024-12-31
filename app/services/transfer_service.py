from fastapi import HTTPException
from app.config import supabase
from app.models.transfer import TransferCreate
from .account_service import AccountService

class TransferService:
    @staticmethod
    async def create_transfer(transfer: TransferCreate):
        try:
            sending_account_balance = await AccountService.get_account_balance_internal(transfer.sending_account_number, transfer.sending_routing_number)
            receiving_account_balance = await AccountService.get_account_balance_internal(transfer.receiving_account_number, transfer.receiving_routing_number)
            if not sending_account_balance:
                raise HTTPException(404, detail="Sender account does not exist")
            if not receiving_account_balance:
                raise HTTPException(404, detail="Receiving account does not exist")
            if sending_account_balance < transfer.transfer_amount:
                transfer.status = "Failed: Insufficient Funds"
                supabase.table("Transfers").insert(transfer.model_dump()).execute()
                raise HTTPException(400, detail="Sending account has insufficient funds")
            if not transfer.transfer_amount > 0:
                raise HTTPException(400, detail="Transfer amount must be non-zero and positive")
            
            await AccountService.update_account_balance(transfer.sending_account_number, transfer.sending_routing_number, -transfer.transfer_amount)
            await AccountService.update_account_balance(transfer.receiving_account_number, transfer.receiving_routing_number, transfer.transfer_amount)

            transfer.status = "Success"
            response = supabase.table("Transfers").insert(transfer.model_dump()).execute()
            return response.data[0]["status"] if response.data else None
        except HTTPException:
            raise
        except Exception as e:
            transfer.status = "Failed: Unexpected Error"
            raise HTTPException(500, detail=f"Transfer failed: {e}")
        
    @staticmethod
    async def get_transfer_history(account_number: str) -> list:
        try:
            if not len(account_number) == 12 or not account_number.isdigit():
                raise HTTPException(status_code=400, detail="Invalid account number")
            
            response = (supabase.table("Transfers")
                        .select("sending_account_number, receiving_account_number, transfer_amount, status").
                        or_(f"sending_account_number.eq.{account_number},receiving_account_number.eq.{account_number}")
                        .execute())
            return response.data
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Transfer fistory failed: {e}")

