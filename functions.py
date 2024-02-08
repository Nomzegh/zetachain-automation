import requests
import time
from web3 import Web3
from eth_account.messages import encode_structured_data
from contracts_abi import pool_abi, approve_abi
from config import (
    RPC,
    BSC_RPC,
    bnb_value_bsc,
    bnb_value_zeta,
    pool_zeta_value,
    bsc_gasprice,
    bnb_to_approve,
    check_user_points_time,
    check_tasks_time,
    claim_tasks_time,
    transactions_break_time,
    enroll_verify_time,
)


web3 = Web3(Web3.HTTPProvider(RPC))


def current_time():
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return cur_time


def generate_signature(private_key: str) -> hex:
    web3 = Web3(Web3.HTTPProvider(RPC))
    msg = {
        "types": {
            "Message": [{"name": "content", "type": "string"}],
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
            ],
        },
        "domain": {"name": "Hub/XP", "version": "1", "chainId": 7000},
        "primaryType": "Message",
        "message": {"content": "Claim XP"},
    }

    encoded_data = encode_structured_data(msg)
    result = web3.eth.account.sign_message(encoded_data, private_key)
    claim_signature = result.signature.hex()

    return claim_signature


def enroll(private_key: str) -> str:
    account = web3.eth.account.from_key(private_key)
    tx = {
        "from": account.address,
        "to": web3.to_checksum_address("0x3C85e0cA1001F085A3e58d55A0D76E2E8B0A33f9"),
        "value": 0,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": web3.eth.gas_price,
        "chainId": 7000,
        "data": "0xb9daad50000000000000000000000000a1f094bb96ccf23ce843b05d0ceb32d2a027875b0000000000000000000000000000000000000000000000000000000065eb22e7000000000000000000000000000000000000000000000000000000000000001c19e0a965ecc7e364205e0694abe5fb72300f53fd6732bcd49dca98c968b3b1ae73f0452fc26d410876c60bf399281663fe628cd88f7ce1eb67015c319a72e5f4",
    }
    tx["gas"] = int(web3.eth.estimate_gas(tx))

    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()

    print(f"{current_time()} | Waiting for Enroll TX to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        print(f"{current_time()} | Transaction {transaction_hash} failed!")
        time.sleep(transactions_break_time)
        return

    print(f"{current_time()} | Enroll (register) hash: {transaction_hash}")
    time.sleep(transactions_break_time)


def enroll_verify(private_key):
    account = web3.eth.account.from_key(private_key)
    print(f"{current_time()} |  Verifying enroll for {account.address}...")

    headers = {
        "authority": "xp.cl04.zetachain.com",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://hub.zetachain.com",
        "Referer": "https://hub.zetachain.com/",
    }
    params = {
        "address": account.address,
    }

    response = requests.post(
        "https://xp.cl04.zetachain.com/v1/enroll-in-zeta-xp",
        headers=headers,
        json=params,
    )
    if response.status_code == 200:
        response = response.json()
        print(f"{current_time()} | Verify status: {response['isUserVerified']}")
        time.sleep(enroll_verify_time)
    else:
        print(f"{current_time()} | Error status code: {response.status_code}")
        time.sleep(enroll_verify_time)


def transfer(private_key: str) -> str:
    account = web3.eth.account.from_key(private_key)
    tx = {
        "from": account.address,
        "to": account.address,
        "value": web3.to_wei(0, "ether"),
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": web3.eth.gas_price,
        "chainId": 7000,
    }
    tx["gas"] = int(web3.eth.estimate_gas(tx))
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    print(f"{current_time()} | Waiting for Self transfer TX to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        print(f"{current_time()} | Transaction {transaction_hash} failed!")
        time.sleep(transactions_break_time)
    print(f"{current_time()} | Send & Receive TX hash: {transaction_hash}")
    time.sleep(transactions_break_time)


def bsc_quest(private_key: str) -> str:
    web3 = Web3(Web3.HTTPProvider(BSC_RPC))
    account = web3.eth.account.from_key(private_key)
    tx = {
        "from": account.address,
        "to": web3.to_checksum_address(
            "0x70e967acFcC17c3941E87562161406d41676FD83"
        ),  # BSC address to bridge bnb -> zeta
        "value": web3.to_wei(bnb_value_bsc, "ether"),
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": web3.to_wei(bsc_gasprice, "gwei"),
        "chainId": 56,
    }
    tx["gas"] = int(web3.eth.estimate_gas(tx))
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    print(f"{current_time()} | Waiting for BSC transfer TX to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        print(f"{current_time()} | Transaction {transaction_hash} failed!")
        time.sleep(transactions_break_time)
    print(f"{current_time()} | Receive BNB from BSC TX: {transaction_hash}")
    time.sleep(transactions_break_time)


def check_user_points(private_key):
    account = web3.eth.account.from_key(private_key)
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://hub.zetachain.com",
            "Connection": "keep-alive",
            "Referer": "https://hub.zetachain.com/",
        }
    )
    params = {
        "address": account.address,
    }

    response = session.get(
        "https://xp.cl04.zetachain.com/v1/get-points",
        params=params,
    )
    if response.status_code == 200:
        response = response.json()
        print(
            f'Address: {account.address}\nRank: {response["rank"]}\nLevel: {response["level"]}\nTotal XP: {response["totalXp"]}\n-----------------'
        )
        time.sleep(check_user_points_time)
    else:
        print(f"{current_time()} | Error: {response.json()}\n----------------")
        time.sleep(check_user_points_time)


def check_tasks(private_key):
    account = web3.eth.account.from_key(private_key)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://hub.zetachain.com",
        "Connection": "keep-alive",
        "Referer": "https://hub.zetachain.com/",
    }
    check_params = {
        "address": account.address,
    }

    check_resp = requests.get(
        "https://xp.cl04.zetachain.com/v1/get-user-has-xp-to-refresh",
        params=check_params,
        headers=headers,
    )
    quests_to_refresh = []
    check_resp = check_resp.json()
    if check_resp["totalAmountToRefresh"] > 0:
        for task, task_data in check_resp["xpRefreshTrackingByTask"].items():
            if task_data["hasXpToRefresh"]:
                quests_to_refresh.append(task)
    time.sleep(check_tasks_time)

    return quests_to_refresh


def claim_tasks(private_key):
    account = web3.eth.account.from_key(private_key)
    quest_list = check_tasks(private_key)
    account = web3.eth.account.from_key(private_key)
    if quest_list == []:
        print(f"{current_time()} | Nothing to claim for address {account.address}")
        time.sleep(claim_tasks_time)
        return

    for quest in quest_list:
        session = requests.Session()
        claim_data = {
            "address": account.address,
            "task": quest,
            "signedMessage": generate_signature(private_key),
        }
        session.headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://hub.zetachain.com",
                "Connection": "keep-alive",
                "Referer": "https://hub.zetachain.com/",
            }
        )
        response = session.post(
            "https://xp.cl04.zetachain.com/v1/xp/claim-task",
            json=claim_data,
        )
        response = response.json()

        print(f"{current_time()} | Claimed {quest} for address {account.address}")
        time.sleep(claim_tasks_time)


def pool_tx(private_key):
    contract = web3.eth.contract(
        address=web3.to_checksum_address("0x2ca7d64A7EFE2D62A725E2B35Cf7230D6677FfEe"),
        abi=pool_abi,
    )
    account = web3.eth.account.from_key(private_key)
    tx = contract.functions.addLiquidityETH(
        web3.to_checksum_address("0x48f80608B672DC30DC7e3dbBd0343c5F02C738Eb"),
        web3.to_wei(bnb_value_zeta, "ether"),
        0,
        0,
        account.address,
        web3.eth.get_block("latest").timestamp + 3600,
    ).build_transaction(
        {
            "from": account.address,
            "value": web3.to_wei(pool_zeta_value, "ether"),
            "nonce": web3.eth.get_transaction_count(account.address),
            "gasPrice": web3.eth.gas_price,
            "chainId": 7000,
        }
    )
    tx["gas"] = int(web3.eth.estimate_gas(tx))
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    print(f"{current_time()} | Waiting for Pool deposit TX to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        print(f"{current_time()} | Transaction {transaction_hash} failed!")
        time.sleep(transactions_break_time)
    print(f"{current_time()} | Pool deposit TX hash: {transaction_hash}")
    time.sleep(transactions_break_time)


def approve(private_key):
    contract = web3.eth.contract(
        address=web3.to_checksum_address("0x48f80608B672DC30DC7e3dbBd0343c5F02C738Eb"),
        abi=approve_abi,
    )
    account = web3.eth.account.from_key(private_key)
    tx = contract.functions.approve(
        web3.to_checksum_address("0x2ca7d64A7EFE2D62A725E2B35Cf7230D6677FfEe"),
        web3.to_wei(bnb_to_approve, "ether"),
    ).build_transaction(
        {
            "from": account.address,
            "value": 0,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gasPrice": web3.eth.gas_price,
            "chainId": 7000,
        }
    )
    tx["gas"] = int(web3.eth.estimate_gas(tx))
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()
    print(f"{current_time()} | Waiting for Approve TX to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        print(f"{current_time()} | Transaction {transaction_hash} failed!")
        time.sleep(transactions_break_time)
    print(f"{current_time()} | Approve hash: {transaction_hash}")
    time.sleep(transactions_break_time)