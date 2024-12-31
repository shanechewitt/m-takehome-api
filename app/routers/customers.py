from fastapi import APIRouter
from app.models.customer import CustomerCreate, Customer
from app.services.customer_service import CustomerService

router = APIRouter()

@router.post("/create", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    return await CustomerService.create_customer(customer)

@router.get("/customer-list", response_model=list)
async def customer_list():
    return await CustomerService.customer_list_get()