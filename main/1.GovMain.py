from tracemalloc import start
from CheckTemplate import check_stage
from composer import Chain
import asyncio
import time

def main() -> None:
    start_time = time.time()
    check_stage(Chain.CheckDepStage().url, Chain.CheckDepStage().status, "dep_stage", "been proposed!")
    check_stage(Chain.CheckVoteStage().url, Chain.CheckVoteStage().status, "vote_stage", "entered the voting stage!")
    check_stage(Chain.CheckApprovedProps().url, Chain.CheckApprovedProps().status, "app_stage", "been approved!")
    check_stage(Chain.CheckRejectedProps().url, Chain.CheckRejectedProps().status, "rej_stage", "been rejected!")
    print(time.time() - start_time)

if __name__ == "__main__":
    main()