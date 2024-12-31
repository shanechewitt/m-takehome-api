from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import supabase
from app.routers import accounts, customers, transfers

app = FastAPI(title="Meow Takehome")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(transfers.router, prefix="/api/transfers", tags=["transfers"])

@app.get("/")
def root():
    return {"message": "Shane Hewitt Meow Takehome"}
