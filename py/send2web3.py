import json
from web3 import Web3
import os
from dotenv import load_dotenv


binance_testnet_rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
web3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url))

#await web3.is_connected()

#print(web3)
#print(f"Is connected: {web3.is_connected()}")  # Is connected: True
print(f"Is connected: {web3.isConnected()}")  # Is connected: True


# ABI из контракта
ERC20_ABI = json.loads('''[
    {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "account",
          "type": "address"
        }
      ],
      "name": "balanceOf",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "decimals",
      "outputs": [
        {
          "internalType": "uint8",
          "name": "",
          "type": "uint8"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "addr",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "mint",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "totalSupply",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]
''')

load_dotenv()
#Load the private keys
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

print(PRIVATE_KEY)

# KZC токен
kzc_contract_address = '0x7FdA984F8Fe8244b1336aadfBd9cAe486C56CFeC'

# инициализация контракта KZC
kzc_contract = web3.eth.contract(kzc_contract_address, abi=ERC20_ABI)
#web3.eth.contract(kzc_contract_address, abi=ERC20_ABI)

# просмотр всех возможных функций
#all_functions = kzc_contract.all_functions()
#print(f"Все функции ERC20 токена:\n{all_functions}")

kzc_decimals = kzc_contract.functions.decimals().call()
#kzc_decimals = web3.eth.contract.function.decimals().call()

print(f"decimals: {kzc_decimals}")

mykzc_addr = "0x00C5d1B9a29232738b5aF5028bb230519D513Da8"
#checksum_addr = Web3.to_checksum_address(mykzc_addr)
checksum_addr = Web3.toChecksumAddress(mykzc_addr)

balance = kzc_contract.functions.balanceOf(checksum_addr).call()
#balance = web3.eth.contract.functions.balanceOf(checksum_addr).call()

balance_1 = balance / pow(10, kzc_decimals)
print(f"balance of {mykzc_addr} = {balance_1}")

#totalsupply = kzc_contract.functions.totalSupply().call()
#totsup = totalsupply / pow(10, kzc_decimals)
#print(f"totalSupply={totsup}")

acct=web3.eth.account.from_key(PRIVATE_KEY)
print(F"current signer={acct.address}")

mint_amt=50

dict_transaction = {
    'chainId': web3.eth.chain_id, 
    'gas': 210000, 
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.getTransactionCount(mykzc_addr),
}

mint = kzc_contract.functions.mint(checksum_addr, mint_amt).buildTransaction(dict_transaction)

# Подписываем
signed_txn = web3.eth.account.signTransaction(mint, PRIVATE_KEY)

# Отправляем, смотрим тут https://testnet.bscscan.com/
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(txn_hash.hex())
