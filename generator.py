import argparse
import datetime

from openpyxl import Workbook
from openpyxl.styles import Alignment

from crypto_util import generate_phrase, derive_sui_address, derive_aptos_address

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

worksheet.append([
    'Address EMV',
    'Address SUI',
    'Address APT',
    'Password',
    'Seed Phrase',
    'Private Key',
])

password = config.password

for i in range(int(config.number)):
    wallet, mnemonic_phrase = generate_phrase()
    private_key = wallet.private_key()
    sui_address = derive_sui_address(private_key)
    apt_address = derive_aptos_address(private_key)

    worksheet.append([
        wallet.address(),  # A
        sui_address,  # B
        apt_address,  # C
        password,  # D
        mnemonic_phrase,  # E
        private_key,  # F
    ])

alignment = Alignment(horizontal='center', vertical='center')
for row in worksheet.rows:
    for cell in row:
        cell.alignment = alignment

output_filename = config.output or f'generated_wallets_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

workbook.save(output_filename)
