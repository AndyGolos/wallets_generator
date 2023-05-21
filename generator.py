import argparse
import datetime

from crypto_util import generate_phrase, phrase_to_eth_wallet, \
    phrase_to_apt_wallet, phrase_to_sui_wallet
from writers import XLSXWriter, CSVWriter

arg_parser = argparse.ArgumentParser(
    prog='wallet_generator.py',
    description='Generate a XLSX file of wallets and seed phrases',
)
arg_parser.add_argument('-o', '--output', help='Output file', default=None)
arg_parser.add_argument('-n', '--number', help='Number of wallets to generate', default=10, type=int)
arg_parser.add_argument('-p', '--password', help='Password for wallets', default='', type=str)
arg_parser.add_argument('-f', '--format', help='Output format', default='xlsx', choices=['xlsx', 'csv'])
config = arg_parser.parse_args()

output_filename = config.output or f'generated_wallets_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

if config.format.lower() == 'xlsx':
    writer = XLSXWriter(output_filename)
elif config.format.lower() == 'csv':
    writer = CSVWriter(output_filename)
else:
    raise Exception(f'Unsupported format: {config.format}')

password = config.password

for i in range(int(config.number)):
    mnemonic_phrase = generate_phrase()

    eth_wallet = phrase_to_eth_wallet(mnemonic_phrase)
    sui_wallet = phrase_to_sui_wallet(mnemonic_phrase)
    apt_wallet = phrase_to_apt_wallet(mnemonic_phrase)
    eth_private_key = eth_wallet.private_key()

    row = [
        i + 1,  # Index
        eth_wallet.address(),
        sui_wallet.address(),
        apt_wallet.address(),
        password,
        mnemonic_phrase,
        eth_wallet.private_key(),
        sui_wallet.private_key(),
        apt_wallet.private_key(),
    ]

    writer.add_row(row)
    print('.', end='', flush=True)

print(' :)')

writer.finalize()
print(f'Wallets saved to {output_filename}')
