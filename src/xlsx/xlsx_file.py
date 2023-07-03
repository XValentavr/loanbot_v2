import pandas as pd
from openpyxl.workbook import Workbook

from cruds.earning_cruds import earnings_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.enums.xlsx_enum import XlsxEnum


def generate_xlsx_file():
    withdraw = pd.DataFrame(withdraw_cruds.get_all_for_xlsx(), columns=['Summa', 'Admin Username', 'Time Created'])
    earnings = pd.DataFrame(earnings_cruds.get_all_for_xlsx(),
                            columns=['Summa', 'Comment', 'Currency', 'Source Name', 'Admin Username', 'Time Created'])

    workbook = Workbook()

    sheet1 = workbook.create_sheet(title='Withdraw')
    _create_rows(sheet1, withdraw)

    sheet2 = workbook.create_sheet(title='Earnings')
    _create_rows(sheet2, earnings)

    output_file = XlsxEnum.NAME
    workbook.save(output_file)

    return output_file


def _create_rows(sheet, table):
    for r, row in enumerate([table.columns] + table.values.tolist(), start=1):
        for c, value in enumerate(row, start=1):
            sheet.cell(row=r, column=c, value=value.replace('\\', '') if isinstance(value, str) else value)
