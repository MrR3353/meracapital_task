import asyncio
import time
from datetime import datetime

import aiohttp

from db import prices, database


class DeribitClient:
    def __init__(self):
        self.base_url = "https://www.deribit.com/api/v2/public/get_index_price"
        # self.base_url = "https://test.deribit.com/api/v2/public/get_index_price"
        self.pairs = ['btc_usd', 'eth_usd']

    async def fetch_price(self, session, ticker):
        url = f"{self.base_url}?index_name={ticker}"
        async with session.get(url, ssl=False) as response:
            if response.status == 200:
                data = await response.json()
                price = data['result']['index_price']
                timestamp = int(time.time())
                await self.save_price(ticker, price, timestamp)
                print(f"Fetched {ticker}: {price} at {datetime.fromtimestamp(timestamp)}")

    async def save_price(self, ticker, price, timestamp):
        query = prices.insert().values(ticker=ticker, price=price, timestamp=timestamp)
        await database.execute(query)

    async def run(self):
        await database.connect()
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [self.fetch_price(session, pair) for pair in self.pairs]
                await asyncio.gather(*tasks)
                await asyncio.sleep(60)


if __name__ == "__main__":
    client = DeribitClient()
    asyncio.run(client.run())