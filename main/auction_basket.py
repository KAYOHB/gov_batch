from unittest import load_tests
import mysql.connector
import logging
from dotenv import load_dotenv
import telebot
import asyncio
import os
import aiohttp
from composer import Chain, TGAPI, TGChatId, SQL_init as init

load_dotenv()

url = Chain.Auction().url + Chain.Auction().status


bot = telebot.TeleBot(TGAPI.Xenon().api_key)

logging.basicConfig(filename='/home/kayo/projects/inj_daily/log.log', encoding='utf-8', level=logging.DEBUG)

db = mysql.connector.connect(
    host=init.InjDB().host,
    user=init.InjDB().user,
    passwd=init.InjDB().passwd,
    database=init.InjDB().database
)
auction = db.cursor(buffered=True)

# def get_tasks(session):
#     denoms = []
#     for denom in denoms:
#         denoms.append(session.get(url, ssl=False))
#     return denom

async def auction_request():
    denoms = []
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        data = await r.json()
        for i in range(len(data["amount"])):
            denom = {
                "round_id" : data["auctionRound"],
                "denom_id" : data["amount"][i]["denom"],
                "amount" : data["amount"][i]["amount"]
            }
            denoms.append(denom)
    return denoms

def update_db(round_id, denom_id, amount):
    logging.info("new bid has been placed")
    sql1 = "INSERT INTO auction_basket (round_id, denom_id, amount) VALUES (%s, %s, %s)"
    val1 = (round_id, denom_id, amount)
    auction.execute(sql1, val1)
    db.commit()

def get_last_db():
    sql = "SELECT round_id FROM auction_basket ORDER BY round_id DESC"
    auction.execute(sql)
    myresult = auction.fetchone()
    return int(myresult[0])

def get_denom(round_id):
    sql = f"SELECT * FROM auction_basket WHERE round_id = {round_id}"
    auction.execute(sql)
    myresult = auction.fetchone()
    return myresult

# async def get_async_db():
#     return await asyncio.to_thread(update_db())

async def main() -> None:
    get_last_db()
    auction_latest = await auction_request()
    if int(auction_latest[0]["round_id"]) > get_last_db():
        for i in range(len(auction_latest)):
            update_db(auction_latest[i]["round_id"], auction_latest[i]["denom_id"], auction_latest[i]["amount"])
    else:
        print("no new round")

asyncio.run(main())
        
