from web3 import Web3, HTTPProvider
import time
import logging


infura_url = 'https://mainnet.infura.io/v3/8b3857f24d314fd8a9608d976b299eb2'
w3 = Web3(HTTPProvider(infura_url))

if w3.is_connected():
    print("Connected to Ethereum node")
else:
    raise ConnectionError("Failed to connect to Ethereum node")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


DAI_CONTRACT_ADDRESS = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
TARGET_WALLETS = [
    '0x5111FBAE3505323c1F1b26630a145b606453e21d', 
    '0xb38A90f14b24ae81Ec0B8f1373694f5B59811D8A',
    '0xaaaaAAAACB71BF2C8CaE522EA5fa455571A74106'
]

MY_WALLET_ADDRESS = '0x890eA3F29754FF5F184FEf30181DC49dA0F0b42B'
MY_PRIVATE_KEY = 'f5205ef9f5857c3bd1064b71a74dd7c5c80accb3653526642f5d688b2a2d3579'

DAI_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_spender",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "totalSupply",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_from",
                "type": "address"
            },
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "_to",
                "type": "address"
            },
            {
                "name": "_value",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "_initialSupply",
                "type": "uint256"
            },
            {
                "name": "_name",
                "type": "string"
            },
            {
                "name": "_symbol",
                "type": "string"
            },
            {
                "name": "_decimals",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "spender",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]

dai_contract = w3.eth.contract(address=DAI_CONTRACT_ADDRESS, abi=DAI_ABI)

def get_latest_block_transactions():
    block = w3.eth.get_block('latest')
    return block.transactions

def buy_dai_token(wallet_address, amount):
    nonce = w3.eth.getTransactionCount(MY_WALLET_ADDRESS)
    txn = dai_contract.functions.transfer(wallet_address, amount).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.toWei('5', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=MY_PRIVATE_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logging.info(f"Bought DAI token for wallet: {wallet_address}, tx: {tx_hash.hex()}")
    return tx_hash


def sell_dai_token(wallet_address, amount):
    nonce = w3.eth.getTransactionCount(wallet_address)
    txn = dai_contract.functions.transferFrom(wallet_address, MY_WALLET_ADDRESS, amount).buildTransaction({
        'chainId': 1,
        'gas': 2000000,
        'gasPrice': w3.toWei('5', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=MY_PRIVATE_KEY)
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Sold DAI token for wallet: {wallet_address}, tx: {tx_hash.hex()}")  
    return tx_hash

def process_transactions(transactions):
    for tx_hash in transactions:
        logging.info(f"Processing transaction: {tx_hash}")
        tx = w3.eth.get_transaction(tx_hash)
        from_address = tx['from'].lower()
        to_address = tx['to'].lower() if tx['to'] else None

        if from_address in [wallet.lower() for wallet in TARGET_WALLETS] or (to_address and to_address in [wallet.lower() for wallet in TARGET_WALLETS]):
            if to_address == DAI_CONTRACT_ADDRESS.lower():
                logging.info(f"Buying DAI token from: {tx['from']}")
                buy_dai_token(tx['from'], w3.toWei(1, 'ether'))
            elif from_address == DAI_CONTRACT_ADDRESS.lower():
                logging.info(f"Selling DAI token to: {tx['to']}")
                sell_dai_token(tx['to'], w3.toWei(1, 'ether'))


def monitor_blockchain():
    while True:
        transactions = get_latest_block_transactions()
        process_transactions(transactions)
        time.sleep(10)
if __name__ == "__main__":
    logging.info("Starting Ethereum transaction monitor")
    monitor_blockchain()

