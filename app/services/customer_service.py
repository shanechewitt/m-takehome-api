from app.config import supabase
from app.models.customer import CustomerCreate

class CustomerService:
    @staticmethod
    async def create_customer(customer: CustomerCreate):
        print("creating customer")
        pass