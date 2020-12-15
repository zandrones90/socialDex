from web3 import Web3


def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/57be1139b06643dbaae823f9975cc24a'))
    address = '0x4A8440062E4d91bFb694673256B707ea5F6A0f57'
    privateKey = '0x483242aa17c635d2f2b3f90fc888f38bc8c46fbc8313ba7a25457ed37bdbdfbc'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice=w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx=w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
        ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId
