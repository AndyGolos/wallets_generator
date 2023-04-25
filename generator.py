import datetime

from mnemonic import Mnemonic
from hdwallet import BIP44HDWallet
from openpyxl import Workbook
from openpyxl.styles import Alignment


workbook = Workbook()

worksheet = workbook.active
worksheet.column_dimensions['A'].width = 50
worksheet.column_dimensions['B'].width = 50
worksheet.column_dimensions['C'].width = 80
worksheet.column_dimensions['D'].width = 80

worksheet.append(['Address', 'Password', 'Seed Phrase', 'Private Key'])

password = ""

for i in range(10):
    mnemonic_phrase = Mnemonic("english").generate(128)
    hd_wallet = BIP44HDWallet(symbol="ETH")
    wallet = hd_wallet.from_mnemonic(mnemonic_phrase)
    worksheet.append([wallet.address(), password, mnemonic_phrase, wallet.private_key()])

alignment = Alignment(horizontal='center', vertical='center')
for row in worksheet.rows:
    for cell in row:
        cell.alignment = alignment

workbook.save(f'generated_wallets_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx')
