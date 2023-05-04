import hashlib

from aptos_sdk.account import AccountAddress
from aptos_sdk.ed25519 import PrivateKey, SigningKey, PublicKey
from hdwallet import BIP44HDWallet
from mnemonic import Mnemonic
from nacl.encoding import HexEncoder


def derive_public_key(private_key_hex: str) -> PublicKey:
    private_key = private_key_hex.encode('utf-8')
    private_key = PrivateKey(
        SigningKey(private_key, HexEncoder)
    )
    public_key = private_key.public_key()
    return public_key


def derive_aptos_address(private_key_hex: str) -> str:
    public_key = derive_public_key(private_key_hex)

    acc = AccountAddress.from_key(public_key)
    return str(acc)


def derive_sui_address(private_key_hex: str) -> str:
    public_key = derive_public_key(private_key_hex)

    mac = hashlib.blake2b(digest_size=32)
    mac.update(bytes.fromhex('00'))
    mac.update(bytes(public_key.key))
    return '0x' + mac.hexdigest()


def generate_phrase():
    mnemonic_phrase = Mnemonic("english").generate(128)
    hd_wallet = BIP44HDWallet(symbol="ETH")
    wallet = hd_wallet.from_mnemonic(mnemonic_phrase)
    return wallet, mnemonic_phrase
