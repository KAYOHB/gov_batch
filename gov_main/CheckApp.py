import mysql.connector
from gov.gov.composer import TGAPI, SQL_init as init, TGChatId
from gov.gov.composer import Chain
import requests
import json
import asyncio
import telebot
import logging

async def check_approved() -> None:
    bot = telebot.TeleBot(TGAPI.Xenon().api_key)

    db = mysql.connector.connect(
        host=init.InjDB().host,
        user=init.InjDB().user,
        passwd=init.InjDB().passwd,
        database=init.InjDB().database
    )
    gov = db.cursor(buffered=True)

    url = Chain.CheckApprovedProps().url + Chain.CheckApprovedProps().status
    r = requests.get(url)
    data = json.loads(r.text)

    sql = "SELECT prop_id FROM app_stage ORDER BY prop_id DESC"
    gov.execute(sql)
    myresult = gov.fetchone()
    print(f"{myresult[0]} is the latest approved proposal_id")

    for i in reversed(range(len(data["proposals"]))):
        if int(data["proposals"][i]["proposal_id"]) > myresult[0]:
            prop_id = int(data["proposals"][i]["proposal_id"])
            sql = "INSERT INTO app_stage (prop_id) VALUE (%s)"
            val = (prop_id, )
            gov.execute(sql, val)
            db.commit()
            cur_proposal = data["proposals"][i]["content"]["description"]
            msg_edit = cur_proposal.replace(r"\n", "\n")
            bot.send_message(chat_id=TGChatId.dojo().chat_id, text=f"🔊Proposal {prop_id} has just been approved!\n\n{msg_edit}\n\nMore information on: https://hub.injective.network/governance/")

if __name__ == "__main__":
    asyncio.run(check_approved())