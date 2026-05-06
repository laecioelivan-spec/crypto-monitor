from sqlalchemy.orm import Session
from . import models

def save_price(db: Session, coin: str, value: float):
    price = models.Price(coin=coin, value=value)
    db.add(price)
    db.commit()
    db.refresh(price)
    return price

def get_prices(db: Session, coin: str):
    return db.query(models.Price).filter(models.Price.coin == coin).all()
