from pydantic import BaseModel

class TransferCreate(BaseModel):
    sending_account_number: str
    sending_routing_number: str
    receiving_account_number: str
    receiving_routing_number: str
    transfer_amount: float
    status: str = "Pending"

class Transfer(BaseModel):
    id: str
    sending_account_number: str
    sending_routing_number: str
    receiving_account_number: str
    receiving_routing_number: str
    transfer_amount: float
    status: str