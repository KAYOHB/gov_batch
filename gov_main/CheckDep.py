import mysql.connector
from composer import TGAPI, SQL_init as init, TGChatId
from composer import Chain
import requests
import json
import asyncio
from datetime import datetime as dt, timezone
import dateutil.parser as dp
import telebot
import logging

async def check_vote() -> None:
    bot = telebot.TeleBot(TGAPI.Xenon().api_key)

    db = mysql.connector.connect(
        host=init.InjDB().host,
        user=init.InjDB().user,
        passwd=init.InjDB().passwd,
        database=init.InjDB().database
    )
    gov = db.cursor(buffered=True)

    url = Chain.CheckVoteStage().url + Chain.CheckVoteStage().status
    r = requests.get(url)
    data = json.loads(r.text)
    vote_end = dp.parse(data["proposals"][0]["voting_end_time"])
    msg = data["proposals"][0]["content"]["description"]
    msg_edit = msg.replace(r"\n", "\n")


    sql = "SELECT prop_id FROM vote_stage ORDER BY prop_id DESC"
    gov.execute(sql)
    myresult = gov.fetchone()
    cur_proposal = data["proposals"][0]["proposal_id"]

    for i in range(len(data["proposals"])):
        if int(data["proposals"][i]["proposal_id"]) > myresult[0]:
            print("nope")
            sql = "INSERT INTO vote_stage (prop_id) VALUES (%s)"
            gov.execute(sql)
            val = int(data["proposals"][i]["proposal_id"])
            myresult = gov.fetchone()
            cur_proposal = data["proposals"][0]["proposal_id"]
            bot.send_message(chat_id=TGChatId.test().chat_id, text=f"Proposal {cur_proposal} has just entered the voting stage!\n\nThe proposal:\n{msg_edit}\n\nMore information on: https://hub.injective.network/governance/")

        else:
            print("no new proposals in voting stage")

if __name__ == "__main__":
    asyncio.run(check_vote())