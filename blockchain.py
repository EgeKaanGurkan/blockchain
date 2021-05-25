import hashlib
import random
import time

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme as pkcScheme


class Transaction:

    def __init__(self, amount, sender, receiver):
        self.amount = amount
        self.sender = sender
        self.receiver = receiver

    def toString(self):
        return "{0}\t{1}\t{2}".format(self.amount, self.sender, self.receiver)


class Block:
    nonce = random.randint(0, 99999999)

    def __init__(self, prevHash, transaction):
        self.prevHash = prevHash
        self.transaction = transaction
        self.timestamp = time.time()

    def toString(self):
        return "{0}\t{1}\t{2}".format(str(self.timestamp), self.transaction.toString(), self.prevHash)

    def hash(self):
        return hashlib.sha256(self.toString().encode()).hexdigest()


class Chain:
    chain = []

    @classmethod
    def __init__(cls):
        cls.chain.append(Block(None, Transaction(100, "GENESIS", "Ege")))  # Genesis block

    @classmethod
    def getLastBlock(cls):
        return cls.chain[len(cls.chain) - 1]

    @classmethod
    def mine(cls, nonce):
        solution = 1
        print("Mining the block...")

        while True:
            hash = hashlib.md5(str(nonce + solution).encode()).hexdigest()
            # print("Trying nonce: " + str(nonce) + "\n" + "Hash: " + hash[0:4] + "\n")
            if hash[0:4] == "0000":
                # print("Mined for nonce: " + str(nonce) + ", solution: " + str(solution) + "\n")
                return solution

            solution += 1

    @classmethod
    def addBlock(cls, transaction, senderPublicKey, signature):

        transactionHash = SHA256.new(transaction.toString().encode())
        verifier = pkcScheme(senderPublicKey)
        try:
            verifier.verify(transactionHash, signature)
            print("Signature for transaction '{}' is valid".format(transaction.toString()))
        except:
            print("Signature is invalid")

        newBlock = Block(cls.getLastBlock().hash(), transaction)
        cls.mine(newBlock.nonce)
        cls.chain.append(newBlock)

    @classmethod
    def toString(cls):
        returnString = ""

        for i in range(len(cls.chain)):
            returnString += "Block {}\nHash: {}\n" \
                            "Previous Hash: {}\nTransaction: {}\n\n".format(i,
                                                                        cls.chain[i].hash(),
                                                                        cls.chain[i].prevHash,
                                                                        cls.chain[i].transaction.toString())

        return returnString


chain = Chain()


class Wallet:

    def __init__(self):
        self.keyPair = RSA.generate(1024)
        self.publicKey = self.keyPair.public_key()
        self.balance = 0

    def sendCrypto(self, amount, receiverPublicKey):
        transaction = Transaction(amount, self.publicKey, receiverPublicKey)

        signer = pkcScheme(self.keyPair)
        signature = signer.sign(SHA256.new(transaction.toString().encode()))
        Chain.addBlock(transaction, self.publicKey, signature)
