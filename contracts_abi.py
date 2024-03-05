pool_abi = [
    {
        "type": "function",
        "name": "addLiquidityETH",
        "inputs": [
            {"name": "_token", "type": "address"},
            {"name": "_amountTokenDesired", "type": "uint256"},
            {"name": "_amountTokenMin", "type": "uint256"},
            {"name": "_amountETHMin", "type": "uint256"},
            {"name": "_to", "type": "address"},
            {"name": "_deadline", "type": "uint256"},
        ],
        "outputs": [],
        "stateMutability": "payable",
        "constant": False,
    }
]

approve_abi = [
    {
        "type": "function",
        "name": "approve",
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_amount", "type": "uint256"},
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
        "constant": False,
    }
]

encoding_contract_abi = [
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "bytes", "name": "path", "type": "bytes"},
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint128", "name": "amount", "type": "uint128"},
                    {
                        "internalType": "uint256",
                        "name": "minAcquired",
                        "type": "uint256",
                    },
                    {"internalType": "uint256", "name": "deadline", "type": "uint256"},
                ],
                "internalType": "struct Swap.SwapAmountParams",
                "name": "params",
                "type": "tuple",
            }
        ],
        "name": "swapAmount",
        "outputs": [
            {"internalType": "uint256", "name": "cost", "type": "uint256"},
            {"internalType": "uint256", "name": "acquire", "type": "uint256"},
        ],
        "stateMutability": "payable",
        "type": "function",
    }
]

multicall_abi = [
    {
        "inputs": [{"internalType": "bytes[]", "name": "data", "type": "bytes[]"}],
        "name": "multicall",
        "outputs": [{"internalType": "bytes[]", "name": "results", "type": "bytes[]"}],
        "stateMutability": "payable",
        "type": "function",
    }
]

accfinance_mint_abi = [
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    }
]

accfinance_stake_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "assets", "type": "uint256"},
            {"internalType": "address", "name": "receiver", "type": "address"},
        ],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

rangeprotocol_pool_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "mintAmount", "type": "uint256"},
            {"internalType": "uint256[2]", "name": "maxAmounts", "type": "uint256[2]"},
        ],
        "name": "mint",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [
            {"internalType": "uint128", "name": "amountXMax", "type": "uint128"},
            {"internalType": "uint128", "name": "amountYMax", "type": "uint128"},
        ],
        "name": "getMintAmounts",
        "outputs": [
            {"internalType": "uint128", "name": "mintAmount", "type": "uint128"},
            {"internalType": "uint128", "name": "amountXUsed", "type": "uint128"},
            {"internalType": "uint128", "name": "amountYUsed", "type": "uint128"},
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
]

badge_mint_abi = [
    {
        "constant": False,
        "inputs": [
            {"internalType": "uint256", "name": "expireAt", "type": "uint256"},
            {"internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"internalType": "uint256", "name": "eventId", "type": "uint256"},
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
        ],
        "name": "buy",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    }
]
