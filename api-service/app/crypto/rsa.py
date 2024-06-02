import os
import base64
from dotenv import load_dotenv
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

load_dotenv()


async def get_rsa_private_key():
    return os.environ['RSA_PRIVATE_KEY']

async def get_rsa_public_key():
    return os.environ['RSA_PUBLIC_KEY']

async def decrypt(encrypted):
    try:
        private_key = RSA.import_key(os.environ['RSA_PRIVATE_KEY'])
        cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        return (cipher_rsa.decrypt(base64.b64decode(encrypted))).decode('utf-8')
    except:
        return None

async def encrypt(plaintext):
    try:
        public_key = RSA.import_key(os.environ['RSA_PUBLIC_KEY'])
        cipher_rsa = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
        return base64.b64encode(cipher_rsa.encrypt(plaintext.encode('utf-8'))).decode('utf-8')
    except:
        return None
