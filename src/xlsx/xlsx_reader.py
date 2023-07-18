import logging

import pandas as pd

from create_engine import session
from cruds.earning_cruds import earnings_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from models.earning_model import EarningsModel
from models.withdraw_model import WithdrawModel

logging.basicConfig(filename="../sample.log", level=logging.ERROR)


class XlsxDataUpdater:
    def __init__(self, file_path):
        self.file_path = file_path

    def update_data_from_xlsx(self):
        df = pd.read_excel(self.file_path, sheet_name='Loans')
        try:
            session.query(EarningsModel).delete()
            session.commit()

            session.query(WithdrawModel).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(e)
            return 'Произошла ошибка'

        for _, row in df.iterrows():
            time_created = row['Time Created']
            summa = row['Summa']
            comment = row['Comment']
            currency = row['Currency']
            source_name = row['Source Name']
            admin_username = row['Admin Username']
            source = row['Source']

            if source == 'withdraw':
                withdraw_cruds.update_withdraw_data(time_created, summa, admin_username)
            elif source == 'earnings':
                earnings_cruds.update_earning_from_xlsx(time_created, summa, comment, currency, source_name,
                                                        admin_username)
        return 'Успешно обновлено'
