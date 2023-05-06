import argparse
import datetime

from openpyxl import Workbook
from openpyxl.styles import Alignment

from crypto_util import generate_phrase, derive_sui_address, derive_aptos_address, phrase_to_eth_wallet, \
    phrase_to_apt_wallet, phrase_to_sui_wallet

arg_parser = argparse.ArgumentParser(
    prog='wallet_generator.py',
    description='Generate a XLSX file of wallets and seed phrases',
)
arg_parser.add_argument('-o', '--output', help='Output file', default=None)
arg_parser.add_argument('-n', '--number', help='Number of wallets to generate', default=10, type=int)
arg_parser.add_argument('-p', '--password', help='Password for wallets', default='', type=str)
config = arg_parser.parse_args()

workbook = Workbook()

worksheet = workbook.active
worksheet.column_dimensions['A'].width = 50
worksheet.column_dimensions['B'].width = 70
worksheet.column_dimensions['C'].width = 70
worksheet.column_dimensions['D'].width = 30
worksheet.column_dimensions['E'].width = 80
worksheet.column_dimensions['F'].width = 80
worksheet.column_dimensions['G'].width = 80
worksheet.column_dimensions['H'].width = 80

worksheet.append([
    'Address EVM',
    'Address SUI',
    'Address APT',
    'Password',
    'Seed Phrase',
    'Private Key EVM',
    'Private Key SUI',
    'Private Key APT',
])

password = config.password

for i in range(int(config.number)):
    mnemonic_phrase = generate_phrase()

    eth_wallet = phrase_to_eth_wallet(mnemonic_phrase)
    sui_wallet = phrase_to_sui_wallet(mnemonic_phrase)
    apt_wallet = phrase_to_apt_wallet(mnemonic_phrase)
    eth_private_key = eth_wallet.private_key()

    worksheet.append([
        eth_wallet.address(),  # A
        sui_wallet.address(),  # B
        apt_wallet.address(),  # C
        password,  # D
        mnemonic_phrase,  # E
        eth_wallet.private_key(),  # F
        sui_wallet.private_key(),  # G
        apt_wallet.private_key(),  # H
    ])

alignment = Alignment(horizontal='center', vertical='center')
for row in worksheet.rows:
    for cell in row:
        cell.alignment = alignment

output_filename = config.output or f'generated_wallets_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

workbook.save(output_filename)
