from fastapi import HTTPException
from app.config import supabase
from app.models.account import AccountCreate
import random

class AccountService:
    @staticmethod
    async def create_account(account: AccountCreate):
        try:
            if not account.name.strip():
                raise HTTPException(status_code=400, detail="Bank account name cannot be empty")
            if account.initial_amount < 0:
                raise HTTPException(status_code=400, detail="Bank account balance cannot be negative")
            
            account_model = AccountService._create_account_model(account)
            response = supabase.table("BankAccounts").insert(account_model).execute()
            return response.data[0] if response.data else None
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Bank account creation failed: {e}")

    @staticmethod
    async def get_account_balance(account_number: str, routing_number: str) -> float:
        try:
            if not len(account_number) == 12 and account_number.isdigit():
                raise HTTPException(status_code=400, detail="Invalid account number")
            if not len(routing_number) == 9 and routing_number.isdigit():
                raise HTTPException(status_code=400, detail="Invalid routing number")
            
            response = (supabase.table("BankAccounts")
                        .select("balance")
                        .eq("account_number", account_number)
                        .eq("routing_number", routing_number)
                        .execute())

            if not response.data:
                raise HTTPException(status_code=404, detail="Bank account not found")
            return response.data[0]["balance"]
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Bank account balance GET failed: {e}")

    # Helpers
    @staticmethod
    def _generate_account_numbers() -> tuple[str, str]:
        account_number = ''.join(str(random.randint(0, 9)) for _ in range(12)) # Random 12 digit number
        routing_number = ''.join(str(random.randint(0, 9)) for _ in range(9)) # Random 9 digit number
        return account_number, routing_number
    
    @staticmethod
    def _create_account_model(account_create: AccountCreate) -> dict:
        account_number, routing_number = AccountService._generate_account_numbers()
        return {
            "customer_id": account_create.customer_id,
            "name": account_create.name,
            "balance": account_create.initial_amount,
            "account_number": account_number,
            "routing_number": routing_number
        }
