from fastapi import APIRouter
from app.models.account import AccountCreate, Account
from app.services.account_service import AccountService

router = APIRouter()

@router.post("/create", response_model=Account)
async def create_account(account: AccountCreate):
    return await AccountService.create_account(account)

@router.get("/get-balance/{account_number}", response_model=float)
async def get_balance(account_number: str, routing_number: str):
    return await AccountService.get_account_balance_web(account_number, routing_number)

@router.get("/accounts-list/{customer_id}", response_model=list)
async def get_accounts_list(customer_id: int):
    return await AccountService.get_accounts_list(customer_id)