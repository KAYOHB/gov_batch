from CheckApp import check_approved
from CheckVote import check_vote
import asyncio

async def main() -> None:
    await check_approved()
    await check_vote()

if __name__ == "__main__":
    asyncio.run(main())