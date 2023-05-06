import json
from web3 import Web3
import os
from dotenv import load_dotenv
from mysql import sql_db
import logging.config
import logging
from send_message import message_dev, message_user
from config import wallet_url, wallet_url_kzc, wallet_url_ltc, my_log_ini_file, dev_chat_id


logging.config.fileConfig(my_log_ini_file, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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

kzc_decimals = kzc_contract.functions.decimals().call()
#kzc_decimals = web3.eth.contract.function.decimals().call()

acct=web3.eth.account.from_key(PRIVATE_KEY)
#print(F"current signer={acct.address}")

s_exp = "https://testnet.bscscan.com/tx/{0}"

dict_transaction = {
    'chainId': web3.eth.chain_id, 
    'gas': 210000, 
    'gasPrice': web3.eth.gas_price,
    'nonce': web3.eth.getTransactionCount(mykzc_addr),
}

cursor = sql_db().cursor
s_sql="SELECT pm.id, pm.chat_id, pm.wallet_from, pm.wallet_to, pm.amount "
s_sql=s_sql+" from payments as pm  "
s_sql=s_sql+" where pm.status = -2 "
s_sql=s_sql+" order by 1"

try:
  cursor.execute(s_sql)
except pymysql.Error as e:
  logger.error(e)
  logger.error(s_sql)
  message_dev(s_sql)
result = cursor.fetchall()
if len(result) > 0:
		for r_rec in result:
			id_pay = r_rec[0]             # ID записи
			chat_id = r_rec[1]            # чат_ид пользователя
			wallet_from = r_rec[2]			  # кошелек откуда списывать
			wallet_to = r_rec[3]			    # кошелек на какой перевести
			amount = r_rec[4]			        # сумма перевода
			checksum_addr = Web3.toChecksumAddress(wallet_to)
			mint = kzc_contract.functions.mint(checksum_addr, amount).buildTransaction(dict_transaction)
			# Подписываем
			signed_txn = web3.eth.account.signTransaction(mint, PRIVATE_KEY)
			# Отправляем
			txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
			sql_db().update_withdraw_bsc(id_pay, txn_hash)
			s_str = s_exp.format(txn_hash)
			message_dev(s_str)
			message_user(s_str, chat_id)

