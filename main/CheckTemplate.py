import mysql.connector
from composer import Chain, TGAPI, SQL_init as init, TGChatId
import requests
import json
import asyncio
import telebot
import logging
import time

def check_stage(url, stage, table, message) -> None:
    bot = telebot.TeleBot(TGAPI.Xenon().api_key)

    logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)

    db = mysql.connector.connect(
        host=init.InjDB().host,
        user=init.InjDB().user,
        passwd=init.InjDB().passwd,
        database=init.InjDB().database
    )
    gov = db.cursor(buffered=True)

    url = url + stage
    r = requests.get(url)
    data = json.loads(r.text)

    sql = f"SELECT prop_id FROM {table} ORDER BY prop_id DESC"
    gov.execute(sql)
    myresult = gov.fetchone()

    try:
        diff = int(data["proposals"][0]["proposal_id"]) - myresult[0]
        for i in range(diff):
            if int(data["proposals"][i]["proposal_id"]) > myresult[0]:
                prop_id = int(data["proposals"][i]["proposal_id"])
                sql = "INSERT INTO {table} (prop_id) VALUE (%s)"
                val = (prop_id, )
                gov.execute(sql, val)
                db.commit()
                cur_proposal = data["proposals"][i]["content"]["description"]
                msg_edit = cur_proposal.replace(r"\n", "\n")
                bot.send_message(chat_id=TGChatId.test().chat_id, text=f"🔊Proposal {prop_id} has just {message}!\n\n{msg_edit}\n\nMore information on: https://hub.injective.network/governance/")
                logging.info(f"{prop_id} has been inserted into table {table}")
    except IndexError as e:
        print("No new proposals from call")

if __name__ == "__main__":
    check_stage(Chain.CheckApprovedProps().url, Chain.CheckApprovedProps().status, "app_stage", "been approved!")
