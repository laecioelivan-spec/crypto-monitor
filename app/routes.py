from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import requests
from .database import SessionLocal
from . import crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/price/{coin}")
def get_price(coin: str, db: Session = Depends(get_db)):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url).json()
    value = response[coin]["usd"]

    crud.save_price(db, coin, value)
    return {"coin": coin, "value": value}

@router.get("/history/{coin}")
def get_history(coin: str, db: Session = Depends(get_db)):
    prices = crud.get_prices(db, coin)
    return [{"value": p.value, "timestamp": p.timestamp} for p in prices]
