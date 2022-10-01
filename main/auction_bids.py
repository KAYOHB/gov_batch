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

async def auction_request():
    async with aiohttp.ClientSession() as session:
        r = await session.get(url)
        data = await r.json()
        print(data["auctionRound"], data["highestBidder"], float(data["highestBidAmount"]))
        return int(data["auctionRound"]), data["highestBidder"], float(data["highestBidAmount"])

def get_last_db():
    sql = "SELECT * FROM auction_bids ORDER BY round_id DESC, bid_amount DESC"
    auction.execute(sql)
    myresult = auction.fetchone()
    print(myresult[0], myresult[2], float(myresult[1]))
    return int(myresult[0]), myresult[2], float(myresult[1])

async def get_async_db():
    return await asyncio.to_thread(get_last_db)

async def main():
    latest_auction = await auction_request()
    latest_db_row = await get_async_db()
    inj_conv = round(latest_auction[2]/float(10**18), 2)

    if latest_auction[0] == latest_db_row[0] and latest_auction[2] == latest_db_row[2]:
        logging.info('no new bids')
    elif latest_auction[0] == latest_db_row[0] and latest_auction[2] > latest_db_row[2] or latest_auction[0] > latest_db_row[0] and latest_auction[2] > 0:
        logging.info("new bid has been placed")
        sql1 = "INSERT INTO auction_bids (round_id, bid_amount, addresss) VALUES (%s, %s, %s)"
        val1 = (latest_auction[0] , latest_auction[2], latest_auction[1])
        auction.execute(sql1, val1)
        db.commit()
        bot.send_message(chat_id=TGChatId.test().chat_id, text=f"🔥Injective Auction #{latest_auction[0]}🔥:\n\n{latest_auction[1][:3]}...{latest_auction[1][-6:]} just placed a bid of:\n{inj_conv} $INJ\n\nMore information at:\nhttps://hub.injective.network/auction/")
    elif latest_auction[0] > latest_db_row[0] and latest_auction[2] == 0:
        logging.info("new round has started with no bids, enter tg message here")

if __name__ == "__main__":
    asyncio.run(main())