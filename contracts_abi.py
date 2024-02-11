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
