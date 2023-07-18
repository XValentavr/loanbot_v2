import logging
import os

from xlsx.xlsx_reader import XlsxDataUpdater

logging.basicConfig(filename="../sample.log", level=logging.ERROR)


def xlsx_handler_helper(message, loan):
    loan.send_message(
        message.chat.id,
        'Загрузите документ',
    )
    loan.register_next_step_handler(message, lambda msg: xlsx_handler_function(msg, loan))


def xlsx_handler_function(message, loan):
    file_path = 'earnings.xlsx'
    try:
        if message.document:
            file_info = loan.get_file(message.document.file_id)
            downloaded_file = loan.download_file(file_info.file_path)

            with open(file_path, 'wb') as f:
                f.write(downloaded_file)
            xlsx_handler = XlsxDataUpdater(file_path)
            message_success = xlsx_handler.update_data_from_xlsx()

            loan.reply_to(message, message_success)
    except Exception as e:
        logging.error(e)
    finally:
        os.remove(file_path)
