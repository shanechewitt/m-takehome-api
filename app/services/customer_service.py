from app.config import supabase
from app.models.customer import CustomerCreate
from fastapi import HTTPException

class CustomerService:
    @staticmethod
    async def create_customer(customer: CustomerCreate):
        try:
            if not customer.name.strip():
                raise HTTPException(status_code=400, detail="Customer name cannot be empty")

            response = supabase.table('Customers').insert(customer.model_dump()).execute()
            return response.data[0] if response.data else None
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Customer creation failed: {e}")