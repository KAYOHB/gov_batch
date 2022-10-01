from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

class SQL_init:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

    @classmethod
    def InjDB(cls):
        return cls(
        host=os.getenv("host"),
        user=os.getenv("user"),
        passwd=os.getenv("passwd"),
        database=os.getenv("database")
        )

class Chain:
    url = "https://lcd.injective.network"
    def __init__(self, status, url):
        self.status = status

    @classmethod
    def CheckDepStage(cls):
        return cls("/cosmos/gov/v1beta1/proposals?proposal_status=1", cls.url)

    @classmethod
    def CheckVoteStage(cls):
        return cls("/cosmos/gov/v1beta1/proposals?proposal_status=2", cls.url)

    @classmethod
    def CheckApprovedProps(cls):
        return cls("/cosmos/gov/v1beta1/proposals?proposal_status=3&pagination.reverse=true", cls.url)

    @classmethod
    def CheckRejectedProps(cls):
        return cls("/cosmos/gov/v1beta1/proposals?proposal_status=4&pagination.reverse=true", cls.url)

    @classmethod
    def Auction(cls):
        return cls("/injective/auction/v1beta1/basket", cls.url)

    @classmethod
    def AuctionPending(cls):
        return cls("/injective/exchange/v1beta1/exchange/subaccountDeposits?subaccount_id=0x1111111111111111111111111111111111111111111111111111111111111111", cls.url)

class TGAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    @classmethod
    def Xenon(cls):
        return cls(os.getenv("api_key"))


class TGChatId:
    def __init__(self, chat_id):
        self.chat_id=chat_id

    @classmethod
    def dojo(cls):
        return cls(os.getenv("dojo"))

    @classmethod
    def test(cls):
        return cls(os.getenv("test"))
