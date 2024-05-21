from fastapi import APIRouter
from typing import List
from app.models import FinancialData  # Import your FinancialData model

router = APIRouter()

@router.get("/api/financial_data", response_model=List[FinancialData])
async def get_financial_data():
    financial_data = await FinancialData.all()
    return financial_data
