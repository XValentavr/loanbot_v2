import pandas as pd
from openpyxl.styles import PatternFill, Font
from openpyxl.utils import get_column_letter
from openpyxl.workbook import Workbook
from pandas import Timestamp

from cruds.earning_cruds import earnings_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from helpers.enums.xlsx_enum import XlsxEnum

earnings_columns = ['Time Created', 'Summa', 'Comment', 'Currency', 'Source Name', 'Admin Username']
withdraw_columns = ['Time Created', 'Summa', 'Admin Username']

currency_mapper = {
    CurrencyEnum.EURO: "€",
    CurrencyEnum.UAH: "UAH",
    CurrencyEnum.DOLLAR: '$'
}


def generate_xlsx_file():
    withdraw = pd.DataFrame(withdraw_cruds.get_all_for_xlsx(), columns=withdraw_columns)
    earnings = pd.DataFrame(earnings_cruds.get_all_for_xlsx(), columns=earnings_columns)

    workbook = Workbook()

    sheet1 = workbook.create_sheet(title='Earnings')
    _adapt_sheet_1(sheet1)

    _create_rows(sheet1, earnings)
    _wrap_text(sheet1, earnings_columns)

    sheet2 = workbook.create_sheet(title='Withdraw')
    _adapt_sheet_2(sheet2)

    _create_rows(sheet2, withdraw)
    _wrap_text(sheet2, withdraw_columns)

    output_file = XlsxEnum.NAME
    sheet_name = 'Sheet'
    workbook.remove(workbook[sheet_name])

    _conditional_formatting(sheet1, earnings)
    _conditional_formatting(sheet2, withdraw, "withdraw")

    earnings_range = f"B1:{get_column_letter(len(earnings.columns))}{len(earnings) + 1}"
    sheet1.auto_filter.ref = earnings_range

    withdraw_range = f"B1:{get_column_letter(len(withdraw.columns))}{len(withdraw) + 1}"
    sheet2.auto_filter.ref = withdraw_range

    # Add filter by Summa in 'Earnings' sheet
    sheet1.auto_filter.add_filter_column(0, [], blank=False)
    sheet1.auto_filter.add_filter_column(0, [">0"])

    # Add filter by Summa in 'Withdraw' sheet
    sheet2.auto_filter.add_filter_column(0, [], blank=False)
    sheet2.auto_filter.add_filter_column(0, [">0"])

    workbook.save(output_file)

    return output_file


def _adapt_sheet_2(sheet):
    sheet.column_dimensions['A'].width = 15
    sheet.row_dimensions[1].height = 20

    sheet.column_dimensions['B'].width = 10
    sheet.row_dimensions[1].height = 10

    sheet.column_dimensions['C'].width = 15
    sheet.row_dimensions[1].height = 20
    sheet.sheet_view.zoomScale = 130


def _adapt_sheet_1(sheet):
    sheet.column_dimensions['A'].width = 15
    sheet.row_dimensions[1].height = 20

    sheet.column_dimensions['B'].width = 10
    sheet.row_dimensions[1].height = 10

    sheet.column_dimensions['C'].width = 50
    sheet.row_dimensions[1].height = 90

    sheet.column_dimensions['D'].width = 15
    sheet.row_dimensions[1].height = 20

    sheet.column_dimensions['E'].width = 15
    sheet.row_dimensions[1].height = 25

    sheet.column_dimensions['F'].width = 15
    sheet.row_dimensions[1].height = 25

    sheet.sheet_view.zoomScale = 130


def _create_rows(sheet, table):
    for r, row in enumerate([table.columns] + table.values.tolist(), start=1):
        for c, value in enumerate(row, start=1):
            if table.columns[c - 1] == 'Summa':  # Check if the column is 'Summa'
                if isinstance(value, str) and value not in withdraw_columns and value not in earnings_columns:
                    value = float(value)
            elif table.columns[c - 1] == 'Time Created':
                if isinstance(value, Timestamp) and value not in withdraw_columns and value not in earnings_columns:
                    value = pd.Timestamp(value).date()
            elif table.columns[c - 1] == 'Source Name':
                if isinstance(value, str) and value not in withdraw_columns and value not in earnings_columns:
                    if value == InlineButtonsHelperEnum.OTHER:
                        value = ''
            elif table.columns[c - 1] == 'Currency':
                if isinstance(value, str) and value not in withdraw_columns and value not in earnings_columns:
                    if value in [currency.value for currency in CurrencyEnum]:
                        value = currency_mapper.get(value)
            sheet.cell(row=r, column=c, value=value.replace('\\', '') if isinstance(value, str) else value)


def _conditional_formatting(sheet, model, model_name: str = None):
    for row in sheet.iter_rows(min_row=2, max_row=len(model) + 1):
        summa_cell = row[earnings_columns.index('Summa')]
        if summa_cell.value < 0 or model_name == 'withdraw':
            summa_cell.font = Font(color="F21F1F")  # Set text color to white for negative values
        else:
            summa_cell.font = Font(color="10EB4B")  # Set text color to black for positive values


def _wrap_text(sheet, columns):
    for column in columns:
        column_letter = chr(ord('A') + columns.index(column))
        for cell in sheet[column_letter]:
            cell.alignment = cell.alignment.copy(wrap_text=True)
