import json
from web3 import Web3

binance_testnet_rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"

web3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url))

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

# KZC токен
kzc_contract_address = '0x7FdA984F8Fe8244b1336aadfBd9cAe486C56CFeC'

# инициализация контракта KZC
kzc_contract = web3.eth.contract(kzc_contract_address, abi=ERC20_ABI)

# просмотр всех возможных функций
#all_functions = kzc_contract.all_functions()
#print(f"Все функции ERC20 токена:\n{all_functions}")

kzc_decimals = kzc_contract.functions.decimals().call()
print(f"decimals: {kzc_decimals}")

mykzc_addr = "0x00C5d1B9a29232738b5aF5028bb230519D513Da8"
checksum_addr = Web3.to_checksum_address(mykzc_addr)

balance = kzc_contract.functions.balanceOf(checksum_addr).call()
balance_1 = balance / pow(10, kzc_decimals)
print(f"balance of {mykzc_addr} = {balance_1}")

#totalsupply = kzc_contract.functions.totalSupply().call()
#totsup = totalsupply / pow(10, kzc_decimals)
#print(f"totalSupply={totsup}")

mint = kzc_contract.functions.mint(checksum_addr, 50).call()

print(mint)
