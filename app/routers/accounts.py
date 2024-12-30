from fastapi import APIRouter
from app.models.account import AccountCreate, Account
from app.services.account_service import AccountService

router = APIRouter()

# Should probably return a slimmer version of the full Account Object i.e. make a CreateAccountResponse object when further along. For now, return full Account obj
@router.post("/create", response_model=Account)
async def create_account(account: AccountCreate):
    return await AccountService.create_account(account)

@router.get("/get-balance/{account_number}", response_model=float)
async def get_balance(account_number: str, routing_number: str):
    return await AccountService.get_account_balance_web(account_number, routing_number)
