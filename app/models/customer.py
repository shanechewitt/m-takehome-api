from pydantic import BaseModel

class CustomerCreate(BaseModel):
    name: str

class Customer(BaseModel):
    id: int
    name: str

class CustomerInfo(BaseModel):
    name: str