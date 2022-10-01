import mysql.connector
import logging
from dotenv import load_dotenv
import telebot
import asyncio
import os
import aiohttp
import time
start_time = time.time()

load_dotenv()

api_key=os.getenv("api_key")
bot = telebot.TeleBot(api_key)

url = "https://lcd.injective.network/injective/oracle/v1beta1/band_ibc_price_states"
url_auction = "https://lcd.injective.network/injective/auction/v1beta1/basket"

db = mysql.connector.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    passwd=os.getenv("passwd"),
    database=os.getenv("database")
)
auction = db.cursor(buffered=True)

async def get_round():
     async with aiohttp.ClientSession() as session:
        r = await session.get(url_auction)
        data = await r.json()
        round = data["auctionRound"]
        return int(round)

async def get_price(symbol):
    if symbol == "WETH":
        symbol = "ETH"
    price = ""
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        data = await r.json()
        for i in range(len(data["price_states"])):
            if data["price_states"][i]["symbol"] == symbol:
                price = data["price_states"][i]["price_state"]["price"]
        return round(float(price), 2)
        
async def get_basket():
    val = await get_round()
    sql = f"SELECT round_id, name, amount/POWER(10,decimals) FROM auction_basket INNER JOIN denoms ON auction_basket.denom_id = denoms.denom_id WHERE round_id = {val}"
    auction.execute(sql, val)
    myresult = auction.fetchall()
    return (myresult)

async def main() -> None:
    name = await get_basket()
    round_now = await get_round()
    sum = 0
    for i in range(len(name)):
        sum = sum + await get_price(name[i][1]) * name[i][2]
    print(f"Total basket for round {round_now} ${round(sum, 2)}", time.time() - start_time)
    bot.send_message(chat_id=-606157239, text=f"🔊Round {round_now} has just begun with a total basket value of:\n${round(sum, 2)}\n\nAssets:\n{name[0][1]}\n{name[1][1]}\n\nWHERE IS PEPE?")
asyncio.run(main())
