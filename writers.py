import abc
import csv

from openpyxl.styles import Alignment
from openpyxl.workbook import Workbook


class AbstractWriter(abc.ABC):
    HEADERS = [
        'Index',
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

        dimensions = [12, 50, 70, 70, 30, 80, 80, 80, 80]
        worksheet = workbook.active
        for i, width in enumerate(dimensions):
            worksheet.column_dimensions[chr(ord('A') + i)].width = width

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
