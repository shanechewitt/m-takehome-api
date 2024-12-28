from fastapi import APIRouter
from app.models.customer import CustomerCreate, Customer
from app.services.customer_service import CustomerService

router = APIRouter()

@router.post("/create-customer", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    return await CustomerService.create_customer(customer)