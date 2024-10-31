from typing import Optional

from fastapi import FastAPI
from sqlalchemy import desc

from app.db import database, prices

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/prices")
async def get_all_prices(ticker: str):
    query = prices.select().where(prices.c.ticker == ticker)
    return await database.fetch_all(query)


@app.get("/latest_price")
async def get_latest_price(ticker: str):
    query = prices.select().where(prices.c.ticker == ticker).order_by(desc(prices.c.timestamp)).limit(1)
    return await database.fetch_one(query)


@app.get("/prices_by_date")
async def get_prices_by_date(ticker: str, start_date: Optional[int] = None, end_date: Optional[int] = None):
    query = prices.select().where(prices.c.ticker == ticker)
    if start_date:
        query = query.where(prices.c.timestamp >= start_date)
    if end_date:
        query = query.where(prices.c.timestamp <= end_date)

    return await database.fetch_all(query)
