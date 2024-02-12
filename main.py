import time
from web3 import Web3
from functions import (
    approve,
    enroll,
    transfer,
    pool_tx,
    bsc_quest,
    claim_tasks,
    check_user_points,
    enroll_verify,
    btc_quest,
    eth_quest,
    bsc_izumi_quest,
)

RPC = "https://zetachain-mainnet-archive.allthatnode.com:8545"
web3 = Web3(Web3.HTTPProvider(RPC))
private_keys = []
proxies = []

with open("keys.txt", "r") as f:
    for line in f:
        line = line.strip()
        private_keys.append(line)

with open("proxies.txt", "r") as p:
    for proxy in p:
        proxy = proxy.strip()
        proxies.append(proxy)


if __name__ == "__main__":
    choice = int(
        input(
            "\n----------------------"
            "\n1: Enroll                    | +2000 XP ONCE"
            "\n2: Enroll verify             "
            "\n3: Send & Receive Zeta quest | +3500 XP"
            "\n4: Receive BNB in ZetaChain  | +2500 XP "
            "\n5: Approve BNB for LP transaction"
            "\n6: LP any core pool          | +5000 XP"
            "\n7: Receive BTC in Zetachain  | +2500 XP"
            "\n8: Receive ETH in Zetachain  | +2500 XP"
            "\n9: Receive BNB (Izumi)       | +2500 XP"
            "\n10: Check total XP|Rank|Level"
            "\n11: Claim all available tasks"
            "\n----------------------"
            "\nChoice: "
        )
    )
    transaction_functions = {
        1: enroll,
        2: enroll_verify,
        3: transfer,
        4: bsc_quest,
        5: approve,
        6: pool_tx,
        7: btc_quest,
        8: eth_quest,
        9: bsc_izumi_quest,
        10: check_user_points,
        11: claim_tasks,
    }

    for key, proxy in zip(private_keys, proxies):
        try:
            if choice in transaction_functions:
                if proxy:
                    transaction_functions[choice](key, proxy)
                else:
                    transaction_functions[choice](key)
            else:
                print(f"Wrong choice number. 1 | 2 | 3 ...")
        except Exception as e:
            error_message = f"Error for address: {web3.eth.account.from_key(key).address} | Error: {e}\n"
            print(error_message)
            time.sleep(3)
            with open("fail_logs.txt", "a") as log_file:
                log_file.write(error_message + f" ")
