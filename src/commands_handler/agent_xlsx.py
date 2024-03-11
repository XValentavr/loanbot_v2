import os

from xlsx.xlsx_file import generate_xlsx_file


def send_xlsx_file(loan, message, partial=False):
    xlsx_file = generate_xlsx_file(partial)

    with open(xlsx_file, 'rb') as file:
        loan.send_document(message.chat.id, file)
    os.remove(xlsx_file)
