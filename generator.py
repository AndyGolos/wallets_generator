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
    mnemonic_object = Mnemonic("english")
    mnemonic_phrase = mnemonic_object.generate(128)
    test = BIP44HDWallet(symbol="ETH")
    wallet = test.from_mnemonic(mnemonic_phrase)
    worksheet.append([wallet.address(), password, mnemonic_phrase, wallet.private_key()])


alignment = Alignment(horizontal='center', vertical='center')
for row in worksheet.rows:
    for cell in row:
        cell.alignment = alignment

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Save the workbook to a file
workbook.save(f'generated_wallets_{timestamp}.xlsx')
