from pydantic import BaseModel

class AccountCreate(BaseModel):
    customer_id: int
    name: str
    initial_amount: float

class Account(BaseModel):
    id: int
    name: str
    customer_id: int
    balance: float
    account_number: str
    routing_number: str

class AccountInfo(BaseModel):
    id: int
    name: str
    account_number: str
    routing_number: str

