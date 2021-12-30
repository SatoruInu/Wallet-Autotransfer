# SIMPLE WALLET AUTO TRANSFER SCRIPT FOR $SATO.
# MADE BY DAYNE / @INFECTIVESHARED
from web3 import Web3
from datetime import datetime
import sys, os

current_time = datetime.now()
current_time = current_time.strftime("%d-%m-%Y %H:%M:%S")

provider = 'https://mainnet.infura.io/v3/TEST'
wallet_key = os.getenv('wallet_key')

sender = '0xTEST1'
receiver = '0xTEST2'
min_transaction = 0.5
gas_gwei = 120

# INITIALIZE WEB3 AND GRAB TRANSACTION COUNT
try:
    w3 = Web3(Web3.HTTPProvider(provider))
    sender_csum = Web3.toChecksumAddress(sender)
    nonce = w3.eth.getTransactionCount(sender_csum)
except Exception as e:
    print(f'[{current_time}] ERROR INITIALIZING WEB3 [{e}]')
    sys.exit()

# CHECK BALANCE
try:
    receiver_csum = Web3.toChecksumAddress(receiver)

    balance = w3.eth.getBalance(sender_csum)
    balance = w3.fromWei(balance, 'ether')

    if (balance > min_transaction):
        print(f'[{current_time}] SENDER HAS {balance} ETH')
        print(f'[{current_time}] SENDING TRANSFER')
    else:
        print(f'[{current_time}] BALANCE DOES NOT REACH {min_transaction} MINIMUM')
        sys.exit()
except Exception as e:
    print(f'[{current_time}] ERROR GETTING BALANCE [{e}]')
    sys.exit()

# SEND TRANSACTION
try:
    tx = {
        'nonce': nonce,
        'to': receiver,
        'value': w3.eth.getBalance(sender_csum),
        #'value': w3.toWei(.002, 'ether'),
        'gas': 21000,
        'gasPrice': w3.toWei(gas_gwei, 'gwei')
    }

    signed_tx = w3.eth.account.signTransaction(tx, wallet_key)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(f'[{current_time}] TRANSACTION SENT [{str(tx_hash).hex()}]')
except Exception as e:
    print(f'[{current_time}] EXCEPTION SENDING TRANSACTION [{e}]')
