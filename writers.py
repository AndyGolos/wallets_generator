import abc
import csv

from openpyxl.styles import Alignment
from openpyxl.workbook import Workbook


class AbstractWriter(abc.ABC):
    HEADERS = [
        'Address EVM',
        'Address SUI',
        'Address APT',
        'Password',
        'Seed Phrase',
        'Private Key EVM',
        'Private Key SUI',
        'Private Key APT',
    ]

    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    @abc.abstractmethod
    def add_row(self, row):
        pass

    @abc.abstractmethod
    def finalize(self):
        pass


class XLSXWriter(AbstractWriter):
    def prepare_workbook(self):
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

        worksheet.append(self.HEADERS)
        return workbook, worksheet

    def __init__(self, filename):
        super().__init__(filename)
        self.workbook, self.worksheet = self.prepare_workbook()

    def add_row(self, row):
        self.worksheet.append(row)

    def finalize(self):
        alignment = Alignment(horizontal='center', vertical='center')
        for row in self.worksheet.rows:
            for cell in row:
                cell.alignment = alignment

        self.workbook.save(self.filename)


class CSVWriter(AbstractWriter):
    def __init__(self, filename):
        super().__init__(filename)
        self.rows = []

    def add_row(self, row):
        self.rows.append(row)

    def finalize(self):
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADERS)
            writer.writerows(self.rows)
            self.rows = []
