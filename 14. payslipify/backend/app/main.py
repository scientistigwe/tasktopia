from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User, FinancialData
from database import get_db
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class FinancialDataRequest(BaseModel):
    user_id: int
    date: datetime
    income: float
    expenses: float
    savings: float

@app.post("/api/income")
def add_income(financial_data: FinancialDataRequest, db: Session = Depends(get_db)):
    db_financial_data = FinancialData(**financial_data.dict())
    db.add(db_financial_data)
    db.commit()
    db.refresh(db_financial_data)
    return {"message": "Income data added successfully"}

# Additional routes for expenses, take-home pay calculations, etc.
