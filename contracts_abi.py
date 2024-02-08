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
