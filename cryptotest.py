import os
import base64
import nacl.pwhash
import nacl.secret
import nacl.utils

def _keygen(password: str): #key generation algorithm, not used outside this file
    """
    Takes a password string and returns a key.

    We don't need to salt the password since we're not storing it anywhere in any form.

    Parameters are hardcoded so you don't have to store or pass them.
    """
    password = password.encode('utf-8')
    kdf = nacl.pwhash.argon2i.kdf
    salt = b'1234567812345678' #salt must be exactly 16 bytes long
    ops = 4 #OPSLIMIT_INTERACTIVE
    mem = 33554432 #MEMLIMIT_INTERACTIVE

    return kdf(nacl.secret.SecretBox.KEY_SIZE, password, salt,
                 opslimit=ops, memlimit=mem)

def encrypt(plaintext: str, password: str) -> bytes:
    """
        pynacl includes the nonce (iv), tag, and ciphertext in the result from box.encrypt.

        According to the pynacl docs, the returned value will be exactly 40 bytes longer
        than the plaintext as it contains the 24 byte random nonce and the 16 byte MAC.
    """
    plaintext = plaintext.encode('utf-8')
    key = _keygen(password)
    box = nacl.secret.SecretBox(key)
    encrypted = box.encrypt(plaintext)
    return encrypted

def decrypt(encrypted: bytes, password: str) -> str:
    """
        We first decrypt the ciphertext using pynacl into a bytes object.

        We then use Python's UTF-8 decoder to convert that to a string.

        This function is only used in sopen.py. It is not used in screate.py.

        WARNING: This function NEEDS to be wrapped in a try-catch block, because decryption and decoding can and will raise exceptions.
    """
    key = _keygen(password)
    box = nacl.secret.SecretBox(key)
    plaintext = box.decrypt(encrypted)
    plaintextstring = plaintext.decode('utf-8')
    return plaintextstring


# test function to test the encrypt/decrypt utility works.
def test():
    """
    usage:

    python3
    from cryptotest import test
    test()
    """

    password = input("Enter your password: ")
    plaintext = input("Enter your plaintext: ")
    wholetext1 = encrypt(
        plaintext,
        password
    )
    decrypted1 = decrypt(
        wholetext1,
        password
    )
    assert(decrypted1 == plaintext)

    wholetext2 = encrypt(
        plaintext,
        password
    )
    assert(wholetext1 != wholetext2)

    decrypted2 = decrypt(
        wholetext2,
        password
    )
    assert(decrypted1 == decrypted2 == plaintext)

    print("All crypto tests passed.")

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   test()
