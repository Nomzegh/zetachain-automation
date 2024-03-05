import time
from urllib.parse import urlparse

import requests
from fake_useragent import UserAgent
from requests.sessions import Session
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.providers.rpc import HTTPProvider
from eth_account.messages import encode_structured_data, encode_defunct

from config import (
    RPC,
    bnb_value_zeta,
    pool_zeta_value,
    bnb_to_approve,
    check_user_points_time,
    check_tasks_time,
    claim_tasks_time,
    transactions_break_time,
    enroll_verify_time,
    zeta_value_btc,
    zeta_value_eth,
    zeta_value_bnb,
    eddy_finance_zeta,
    acc_finance_zeta,
    range_protocol_zeta,
    zetaswap_zeta,
)
from contracts_abi import (
    pool_abi,
    approve_abi,
    encoding_contract_abi,
    multicall_abi,
    accfinance_mint_abi,
    accfinance_stake_abi,
    rangeprotocol_pool_abi,
    badge_mint_abi,
)


def current_time():
    cur_time = time.strftime("%Y-%m-%d %H:%M:%S")[:-3]
    return cur_time


def create_web3_with_proxy(rpc_endpoint, proxy=None):
    if proxy is None:
        return Web3(Web3.HTTPProvider(rpc_endpoint))

    proxy_settings = {
        "http": proxy,
        "https": proxy,
    }

    session = Session()
    session.proxies = proxy_settings

    custom_provider = HTTPProvider(rpc_endpoint, session=session)
    web3 = Web3(custom_provider)
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3


def extract_ip_from_proxy(proxy):
    if proxy.startswith("http://"):
        proxy = proxy[7:]
    elif proxy.startswith("https://"):
        proxy = proxy[8:]

    at_split = proxy.split("@")[-1]
    ip = at_split.split(":")[0]

    return ip


def create_session(proxy=None, check_proxy=False):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": UserAgent().random,
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://hub.zetachain.com",
            "Connection": "keep-alive",
            "Referer": "https://hub.zetachain.com/",
        }
    )

    if proxy:
        session.proxies = {"http": proxy, "https": proxy}

    if check_proxy and proxy:
        try:
            proxy_ip = extract_ip_from_proxy(proxy)
            actual_ip = session.get("https://api.ipify.org").text
            if actual_ip != proxy_ip:
                raise Exception(
                    f"Error: Proxy IP ({proxy_ip}) does not match actual IP ({actual_ip}). Stopping script."
                )

            else:
                print(f"Proxy check passed: {actual_ip}")
        except requests.RequestException as e:
            raise Exception(f"Error during proxy check: {e}")

    return session


def estimate_gas_and_send(web3, tx, private_key, tx_name):
    tx["gas"] = int(web3.eth.estimate_gas(tx))
    signed_txn = web3.eth.account.sign_transaction(tx, private_key)
    transaction_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction).hex()

    print(f"{current_time()} | Waiting {tx_name} to complete...")
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)
    if receipt.status != 1:
        print(f"{current_time()} | Transaction {transaction_hash} failed!")
        time.sleep(transactions_break_time)
        return

    print(f"{current_time()} | {tx_name} hash: {transaction_hash}")
    time.sleep(transactions_break_time)


def create_transaction(web3, private_key, tx_name, to, value, data):
    account = web3.eth.account.from_key(private_key)
    tx = {
        "from": account.address,
        "to": web3.to_checksum_address(to),
        "value": value,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gasPrice": web3.eth.gas_price,
        "chainId": 7000,
        "data": data,
    }
    estimate_gas_and_send(web3, tx, private_key, tx_name)


def generate_signature(private_key: str, proxy=None) -> hex:
    web3 = create_web3_with_proxy(RPC, proxy)
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


def enroll(private_key: str, proxy=None) -> str:
    web3 = create_web3_with_proxy(RPC, proxy)
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="Enroll Transaction",
        to="0x3C85e0cA1001F085A3e58d55A0D76E2E8B0A33f9",
        value=0,
        data="0xb9daad50000000000000000000000000a1f094bb96ccf23ce843b05d0ceb32d2a027875b0000000000000000000000000000000000000000000000000000000065eb22e7000000000000000000000000000000000000000000000000000000000000001c19e0a965ecc7e364205e0694abe5fb72300f53fd6732bcd49dca98c968b3b1ae73f0452fc26d410876c60bf399281663fe628cd88f7ce1eb67015c319a72e5f4",
    )


def enroll_verify(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    print(f"{current_time()} |  Verifying enroll for {account.address}...")
    session = create_session(proxy=proxy, check_proxy=True)
    response = session.post(
        "https://xp.cl04.zetachain.com/v1/enroll-in-zeta-xp",
        json={
            "address": account.address,
        },
    )
    if response.status_code == 200:
        response = response.json()
        print(f"{current_time()} | Verify status: {response['isUserVerified']}")
        time.sleep(enroll_verify_time)
    else:
        print(f"{current_time()} | Error status code: {response.status_code}")
        time.sleep(enroll_verify_time)


def transfer(private_key: str, proxy=None) -> str:
    web3 = create_web3_with_proxy(RPC, proxy)
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="Send & Receive ZETA TX",
        to=web3.eth.account.from_key(private_key).address,
        value=0,
        data="0x",
    )


def check_user_points(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    session = create_session(proxy, check_proxy=True)

    response = session.get(
        "https://xp.cl04.zetachain.com/v1/get-points",
        params={
            "address": account.address,
        },
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


def check_tasks(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    session = create_session(proxy=proxy, check_proxy=True)

    check_resp = session.get(
        "https://xp.cl04.zetachain.com/v1/get-user-has-xp-to-refresh",
        params={
            "address": account.address,
        },
    )
    quests_to_refresh = []
    check_resp = check_resp.json()
    if check_resp["totalAmountToRefresh"] > 0:
        for task, task_data in check_resp["xpRefreshTrackingByTask"].items():
            if task_data["hasXpToRefresh"]:
                quests_to_refresh.append(task)
    time.sleep(check_tasks_time)

    return quests_to_refresh


def claim_tasks(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    session = create_session(proxy=proxy, check_proxy=True)
    quest_list = check_tasks(private_key, proxy=proxy)

    if quest_list == []:
        print(f"{current_time()} | Nothing to claim for address {account.address}")
        time.sleep(claim_tasks_time)
        return

    for quest in quest_list:
        claim_data = {
            "address": account.address,
            "task": quest,
            "signedMessage": generate_signature(private_key),
        }
        response = session.post(
            "https://xp.cl04.zetachain.com/v1/xp/claim-task",
            json=claim_data,
        )
        response = response.json()

        print(f"{current_time()} | Claimed {quest} for address {account.address}")
        time.sleep(claim_tasks_time)


def pool_tx(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    contract = web3.eth.contract(
        address=web3.to_checksum_address("0x2ca7d64A7EFE2D62A725E2B35Cf7230D6677FfEe"),
        abi=pool_abi,
    )
    account = web3.eth.account.from_key(private_key)
    data = contract.encodeABI(
        fn_name="addLiquidityETH",
        args=[
            web3.to_checksum_address("0x48f80608B672DC30DC7e3dbBd0343c5F02C738Eb"),
            web3.to_wei(bnb_value_zeta, "ether"),
            0,
            0,
            account.address,
            web3.eth.get_block("latest").timestamp + 3600,
        ],
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="Pool Deposit TX",
        to=contract.address,
        value=web3.to_wei(pool_zeta_value, "ether"),
        data=data,
    )


def approve(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    contract = web3.eth.contract(
        address=web3.to_checksum_address("0x48f80608B672DC30DC7e3dbBd0343c5F02C738Eb"),
        abi=approve_abi,
    )
    data = contract.encodeABI(
        fn_name="approve",
        args=[
            web3.to_checksum_address("0x2ca7d64A7EFE2D62A725E2B35Cf7230D6677FfEe"),
            web3.to_wei(bnb_to_approve, "ether"),
        ],
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="Approve for Pool TX",
        to=contract.address,
        value=0,
        data=data,
    )


def btc_quest(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    contract_for_encoding = web3.eth.contract(
        address=web3.to_checksum_address("0x8Afb66B7ffA1936ec5914c7089D50542520208b8"),
        abi=encoding_contract_abi,
    )
    main_contract = web3.eth.contract(
        address=web3.to_checksum_address("0x34bc1b87f60e0a30c0e24FD7Abada70436c71406"),
        abi=multicall_abi,
    )
    encoded_data = contract_for_encoding.encodeABI(
        fn_name="swapAmount",
        args=[
            (
                b"_\x0b\x1a\x82t\x9c\xb4\xe2'\x8e\xc8\x7f\x8b\xf6\xb6\x18\xdcq\xa8\xbf\x00'\x10|\x8d\xda\x80\xbb\xbe\x12T\xa7\xaa\xcf2\x19\xeb\xe1H\x1cn\x01\xd7\x00'\x10_\x0b\x1a\x82t\x9c\xb4\xe2'\x8e\xc8\x7f\x8b\xf6\xb6\x18\xdcq\xa8\xbf\x00'\x10\x13\xa0\xc5\x93\x0c\x02\x85\x11\xdc\x02f^r\x85\x13Km\x11\xa5\xf4",
                account.address,
                web3.to_wei(zeta_value_btc, "ether"),
                3,
                web3.eth.get_block("latest").timestamp + 3600,
            )
        ],
    )
    tx_data = main_contract.encodeABI(
        fn_name="multicall", args=[[encoded_data, "0x12210e8a"]]
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="BTC Quest TX",
        to="0x34bc1b87f60e0a30c0e24FD7Abada70436c71406",
        value=web3.to_wei(zeta_value_btc, "ether"),
        data=tx_data,
    )


def eth_quest(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    contract_for_encoding = web3.eth.contract(
        address=web3.to_checksum_address("0x8Afb66B7ffA1936ec5914c7089D50542520208b8"),
        abi=encoding_contract_abi,
    )
    main_contract = web3.eth.contract(
        address=web3.to_checksum_address("0x34bc1b87f60e0a30c0e24FD7Abada70436c71406"),
        abi=multicall_abi,
    )
    encoded_data = contract_for_encoding.encodeABI(
        fn_name="swapAmount",
        args=[
            (
                b"_\x0b\x1a\x82t\x9c\xb4\xe2'\x8e\xc8\x7f\x8b\xf6\xb6\x18\xdcq\xa8\xbf\x00\x0b\xb8\x91\xd4\xf0\xd5@\x90\xdf-\x81\xe84\xc3\xc8\xceq\xc6\xc8e\xe7\x9f\x00\x0b\xb8\xd9{\x1d\xe3a\x9e\xd2\xc6\xbe\xb3\x86\x01G\xe3\x0c\xa8\xa7\xdc\x98\x91",
                account.address,
                web3.to_wei(zeta_value_eth, "ether"),
                10,
                web3.eth.get_block("latest").timestamp + 3600,
            )
        ],
    )
    tx_data = main_contract.encodeABI(
        fn_name="multicall", args=[[encoded_data, "0x12210e8a"]]
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="ETH Quest TX",
        to="0x34bc1b87f60e0a30c0e24FD7Abada70436c71406",
        value=web3.to_wei(zeta_value_eth, "ether"),
        data=tx_data,
    )


def bsc_izumi_quest(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    contract_for_encoding = web3.eth.contract(
        address=web3.to_checksum_address("0x8Afb66B7ffA1936ec5914c7089D50542520208b8"),
        abi=encoding_contract_abi,
    )
    main_contract = web3.eth.contract(
        address=web3.to_checksum_address("0x34bc1b87f60e0a30c0e24FD7Abada70436c71406"),
        abi=multicall_abi,
    )
    encoded_data = contract_for_encoding.encodeABI(
        fn_name="swapAmount",
        args=[
            (
                b"_\x0b\x1a\x82t\x9c\xb4\xe2'\x8e\xc8\x7f\x8b\xf6\xb6\x18\xdcq\xa8\xbf\x00'\x10H\xf8\x06\x08\xb6r\xdc0\xdc~=\xbb\xd04<_\x02\xc78\xeb",
                account.address,
                web3.to_wei(zeta_value_bnb, "ether"),
                10,
                web3.eth.get_block("latest").timestamp + 3600,
            )
        ],
    )
    tx_data = main_contract.encodeABI(
        fn_name="multicall", args=[[encoded_data, "0x12210e8a"]]
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="BNB (Izumi Finance) quest",
        to="0x34bc1b87f60e0a30c0e24FD7Abada70436c71406",
        value=web3.to_wei(zeta_value_bnb, "ether"),
        data=tx_data,
    )


def eddy_finance(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="ZETA -> BNB.BSC (Eddy Finance)",
        to="0xDE3167958Ad6251E8D6fF1791648b322Fc6B51bD",
        value=web3.to_wei(eddy_finance_zeta, "ether"),
        data="0x148e6bcc0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000000020000000000000000000000005f0b1a82749cb4e2278ec87f8bf6b618dc71a8bf00000000000000000000000048f80608b672dc30dc7e3dbbd0343c5f02c738eb",
    )


def accumulated_finance(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    accfinance_contract = web3.eth.contract(
        address=web3.to_checksum_address("0xcf1A40eFf1A4d4c56DC4042A1aE93013d13C3217"),
        abi=accfinance_mint_abi,
    )
    stzeta_stake_contract = web3.eth.contract(
        address=web3.to_checksum_address("0x7AC168c81F4F3820Fa3F22603ce5864D6aB3C547"),
        abi=accfinance_stake_abi,
    )
    data = accfinance_contract.encodeABI(
        fn_name="deposit",
        args=[
            account.address,
        ],
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="stZETA Mint",
        to=accfinance_contract.address,
        value=web3.to_wei(acc_finance_zeta, "ether"),
        data=data,
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="stZETA Approve for staking",
        to="0xcba2aeEc821b0B119857a9aB39E09b034249681A",
        value=0,
        data="0x095ea7b30000000000000000000000007ac168c81f4f3820fa3f22603ce5864d6ab3c547ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    )

    stake_data = stzeta_stake_contract.encodeABI(
        fn_name="deposit",
        args=[web3.to_wei(acc_finance_zeta, "ether"), account.address],
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="stZETA Staking",
        to=stzeta_stake_contract.address,
        value=0,
        data=stake_data,
    )


def range_protocol(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    session = create_session(proxy=proxy, check_proxy=True)
    json_data = {
        "query": "\n      query getVaultItemById($vaultId: String) {\n        vault(id: $vaultId) {\n          \n  id\n  liquidity\n  balance0\n  balance1\n  totalSupply\n  totalFeesEarned0\n  totalFeesEarned1\n  tokenX\n  tokenY\n  firstMintAtBlock\n  managerBalanceX\n  managerBalanceY\n  name\n  tag\n  pool\n\n          managingFee\n          performanceFee\n        }\n      }\n    ",
        "variables": {
            "vaultId": "0x08F4539f91faA96b34323c11C9B00123bA19eef3",
        },
        "operationName": "getVaultItemById",
    }

    response = session.post(
        "https://api.goldsky.com/api/public/project_clm97huay3j9y2nw04d8nhmrt/subgraphs/zetachain-izumi/0.2/gn",
        json=json_data,
    ).json()

    balance0 = int(response["data"]["vault"]["balance0"])
    balance1 = int(response["data"]["vault"]["balance1"])
    pool_balance = int(response["data"]["vault"]["balance0"]) + int(
        response["data"]["vault"]["balance1"]
    )
    part0 = balance0 / pool_balance
    part1 = balance1 / pool_balance

    stzeta_amount = int(web3.to_wei(range_protocol_zeta, "ether") * part0)
    wzeta_amount = int(web3.to_wei(range_protocol_zeta, "ether") * part1)

    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="ZETA -> stZETA Swap",
        to="0x45334a5B0a01cE6C260f2B570EC941C680EA62c0",
        value=int(stzeta_amount * 0.95),
        data="0x5bcb2fc6",
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="ZETA deposit to WZETA",
        to="0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf",
        value=int(wzeta_amount * 0.95),
        data="0xd0e30db0",
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="stZETA Approve",
        to="0x45334a5b0a01ce6c260f2b570ec941c680ea62c0",
        value=0,
        data="0x095ea7b300000000000000000000000008f4539f91faa96b34323c11c9b00123ba19eef3ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="wZETA Approve",
        to="0x5f0b1a82749cb4e2278ec87f8bf6b618dc71a8bf",
        value=0,
        data="0x095ea7b300000000000000000000000008f4539f91faa96b34323c11c9b00123ba19eef3ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    )

    range_protocol_contract = web3.eth.contract(
        address=web3.to_checksum_address("0x08F4539f91faA96b34323c11C9B00123bA19eef3"),
        abi=rangeprotocol_pool_abi,
    )

    amounts = range_protocol_contract.functions.getMintAmounts(
        int(stzeta_amount * 0.5), int(stzeta_amount * 0.5)
    ).call()
    data = range_protocol_contract.encodeABI(
        fn_name="mint",
        args=[amounts[2], [amounts[0], amounts[1]]],
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="stZETA & wZETA Pool Deposit",
        to=range_protocol_contract.address,
        value=0,
        data=data,
    )


def mint_badge(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    session = create_session(proxy=proxy, check_proxy=True)
    session.headers.update(
        {
            "ul-auth-api-key": "bWlzc2lvbl9ydW5uZXJAZFd4MGFYWmxjbk5s",
            "Origin": "https://mission.ultiverse.io",
            "Referer": "https://mission.ultiverse.io/",
        }
    )
    response = session.post(
        "https://toolkit.ultiverse.io/api/user/signature",
        json={
            "address": account.address,
            "feature": "assets-wallet-login",
            "chainId": 7000,
        },
    ).json()

    json_data = {
        "address": account.address,
        "signature": account.sign_message(
            encode_defunct(text=response["data"]["message"])
        ).signature.hex(),
        "chainId": 7000,
    }
    response = session.post(
        "https://toolkit.ultiverse.io/api/wallets/signin",
        json=json_data,
    ).json()
    access_token = response["data"]["access_token"]
    session.cookies.update({"Ultiverse_Authorization": access_token})
    session.headers.update(
        {
            "Authority": "mission.ultiverse.io",
            "Referer": "https://mission.ultiverse.io/t/ZmluZHBhdGh8MTcwNjg2MDczMTkzMQ==",
            "ul-auth-token": access_token,
        }
    )
    response = session.post(
        "https://mission.ultiverse.io/api/tickets/mint",
        json={
            "eventId": 10,
            "address": account.address,
        },
    ).json()
    badge_contract = web3.eth.contract(
        address=web3.to_checksum_address(response["data"]["contract"]),
        abi=badge_mint_abi,
    )
    data = badge_contract.encodeABI(
        fn_name="buy",
        args=[
            int(response["data"]["expireAt"]),
            int(response["data"]["tokenId"]),
            int(response["data"]["eventId"]),
            response["data"]["signature"],
        ],
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="ZETA Badge Mint",
        to=badge_contract.address,
        value=0,
        data=data,
    )


def zetaswap_quest(private_key: str, proxy=None):
    web3 = create_web3_with_proxy(RPC, proxy)
    account = web3.eth.account.from_key(private_key)
    session = create_session(proxy=proxy, check_proxy=True)
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="ZETA -> wZETA SWAP",
        to=web3.to_checksum_address("0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf"),
        value=web3.to_wei(zetaswap_zeta, "ether"),
        data="0xd0e30db0",
    )
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="Approve wZETA",
        to=web3.to_checksum_address("0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf"),
        value=0,
        data="0x095ea7b3000000000000000000000000c6f7a7ba5388bfb5774bfaa87d350b7793fd9ef1ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    )
    session.headers.update(
        {
            "authority": "newapi.native.org",
            "api_key": "7e5e5cc85bb10c1a7c5b2836b55e00acfe0a9509",
            "apikey": "7e5e5cc85bb10c1a7c5b2836b55e00acfe0a9509",
            "Origin": "https://app.zetaswap.com",
            "Referer": "https://app.zetaswap.com/",
        }
    )
    response = session.get(
        "https://newapi.native.org/v1/firm-quote",
        params={
            "src_chain": "zetachain",
            "dst_chain": "zetachain",
            "token_in": "0x5F0b1a82749cb4E2278EC87F8BF6B618dC71a8bf",
            "token_out": "0xd97b1de3619ed2c6beb3860147e30ca8a7dc9891",
            "amount": zetaswap_zeta,
            "address": account.address,
            "slippage": "2",
        },
    ).json()
    create_transaction(
        web3=web3,
        private_key=private_key,
        tx_name="wZETA -> ETH.ETH SWAP",
        to=response["txRequest"]["target"],
        value=0,
        data=response["txRequest"]["calldata"],
    )
