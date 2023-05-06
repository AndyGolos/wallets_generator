import hashlib
import hmac
import struct

from aptos_sdk.account import AccountAddress, Account
from aptos_sdk.ed25519 import PrivateKey, SigningKey, PublicKey
from ecdsa.curves import Ed25519
from hdwallet import BIP44HDWallet
from mnemonic import Mnemonic
from nacl.encoding import HexEncoder

BIP39_PBKDF2_ROUNDS = 2048
BIP39_SALT_MODIFIER = "mnemonic"
BIP32_PRIVDEV = 0x80000000
BIP32_SEED_ED25519 = b'ed25519 seed'
APTOS_DERIVATION_PATH = "m/44'/637'/0'/0'/0'"
SUI_DERIVATION_PATH = "m/44'/784'/0'/0'/0'"


class PublicKey25519:
    def __init__(self, private_key):
        self.private_key = private_key

    def __bytes__(self):
        sk = Ed25519.SigningKey(self.private_key)
        return '\x00' + sk.get_verifying_key().to_bytes()


class PublicKeyUtils:
    def __init__(self, words, str_derivation_path=APTOS_DERIVATION_PATH, curve=Ed25519, modifier=BIP32_SEED_ED25519):
        self.privdev = BIP32_PRIVDEV
        self.curve = curve
        self.str_derivation_path = str_derivation_path
        self.modifier = modifier

        self._private_key = self.mnemonic_to_private_key(words)
        self.public_key = PublicKey25519(self._private_key)

    def private_key(self):
        return self._private_key.hex()

    def derive_bip32childkey(self, parent_key, parent_chain_code, i):
        assert len(parent_key) == 32
        assert len(parent_chain_code) == 32
        k = parent_chain_code
        if (i & self.privdev) != 0:
            key = b'\x00' + parent_key
        else:
            key = bytes(PublicKey25519(parent_key))

        d = key + struct.pack('>L', i)

        h = hmac.new(k, d, hashlib.sha512).digest()
        key, chain_code = h[:32], h[32:]

        return key, chain_code

    def mnemonic_to_bip39seed(self, mnemonic, passphrase):
        mnemonic = bytes(mnemonic, 'utf8')
        salt = bytes(BIP39_SALT_MODIFIER + passphrase, 'utf8')
        return hashlib.pbkdf2_hmac('sha512', mnemonic, salt, BIP39_PBKDF2_ROUNDS)

    def mnemonic_to_private_key(self, mnemonic, passphrase=""):
        derivation_path = self.parse_derivation_path()
        bip39seed = self.mnemonic_to_bip39seed(mnemonic, passphrase)
        master_private_key, master_chain_code = self.bip39seed_to_bip32masternode(bip39seed)
        private_key, chain_code = master_private_key, master_chain_code
        for i in derivation_path:
            private_key, chain_code = self.derive_bip32childkey(private_key, chain_code, i)
        return private_key

    def bip39seed_to_bip32masternode(self, seed):
        k = seed
        h = hmac.new(self.modifier, seed, hashlib.sha512).digest()
        key, chain_code = h[:32], h[32:]
        return key, chain_code

    def parse_derivation_path(self):
        path = []
        if self.str_derivation_path[0:2] != 'm/':
            raise ValueError("Can't recognize derivation path. It should look like \"m/44'/chaincode/change'/index\".")
        for i in self.str_derivation_path.lstrip('m/').split('/'):
            if "'" in i:
                path.append(self.privdev + int(i[:-1]))
            else:
                path.append(int(i))

        return path

    def address(self):
        acc = Account.load_key(self._private_key.hex())
        return acc.address().hex()


class SUIPublicKeyUtils(PublicKeyUtils):
    def address(self):
        return derive_sui_address(self.private_key())


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
    return mnemonic_phrase


def phrase_to_eth_wallet(mnemonic_phrase):
    hd_wallet = BIP44HDWallet(symbol="ETH")
    wallet = hd_wallet.from_mnemonic(mnemonic_phrase)
    return wallet


def phrase_to_apt_wallet(mnemonic_phrase):
    return PublicKeyUtils(mnemonic_phrase)


def phrase_to_sui_wallet(mnemonic_phrase):
    return SUIPublicKeyUtils(mnemonic_phrase, str_derivation_path=SUI_DERIVATION_PATH)
