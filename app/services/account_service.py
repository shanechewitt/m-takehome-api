from app.config import supabase
from app.models.account import AccountCreate

class AccountService:
    @staticmethod
    async def create_account(account: AccountCreate):
        print("creating account")
        pass
