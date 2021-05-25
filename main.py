from blockchain import *

if __name__ == '__main__':
    ege = Wallet()
    satoshi = Wallet()
    drake = Wallet()

    ege.sendCrypto(100, satoshi.publicKey)
    satoshi.sendCrypto(50, drake.publicKey)
    overviewText = "Overview of the Blockchain:"
    print("\n" + overviewText)
    print("-" * len(overviewText))
    print(Chain.toString())

    exit(0)