from pydantic import BaseModel

class AccountCreate(BaseModel):
    customer_id: str
    name: str
    initial_amount: float

class Account(BaseModel):
    id: str
    name: str
    customer_id: str
    balance: float
    account_number: str
    routing_number: str


