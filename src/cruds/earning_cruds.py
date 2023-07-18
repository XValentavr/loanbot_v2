import logging
import uuid
from datetime import timedelta
from typing import Optional

from sqlalchemy import asc, desc, null, text
from sqlalchemy import literal
import math

from create_engine import session
from cruds.agent_cruds import agent_cruds
from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.enums.currency_enum import CurrencyEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from models.admins import LoanAdminsModel
from models.earning_model import EarningsModel
from models.sources_of_income_model import SourcesOfIncomeModel
from models.withdraw_model import WithdrawModel


class EarningsCruds:
    @staticmethod
    def insert_source(summa: str, comment: str, agent_id: Optional[str], source_id: Optional[str], currency: str,
                      is_other_source: str):
        source_name = source_of_income_cruds.get_source_by_source_id(source_id)
        source = EarningsModel(
            summa=summa,
            comment=comment,
            agent_source_id=agent_id,
            admin_char=agent_cruds.get_by_id(agent_id).admin_username,
            income_source_id=source_id,
            currency=currency,
            is_other_source=is_other_source,
            source_name=source_name.source,
            source_percent=source_name.percent,
        )

        source.id = uuid.uuid4()

        session.add(source)
        session.commit()
        return source

    @staticmethod
    def get_earning_by_agent_id(agent_id: uuid.UUID) -> EarningsModel:
        return (
            session.query(EarningsModel).order_by(desc(EarningsModel.time_created)).filter(
                EarningsModel.agent_source_id == agent_id).all()
        )

    @staticmethod
    def get_earnings_history_by_date(agent_id: uuid.UUID, start: int, end: int, date_to_check) -> EarningsModel:
        if isinstance(date_to_check, list):
            interval_start = date_to_check[0].strftime("%Y-%m-%d")
            interval_end = (date_to_check[1] + timedelta(days=1)).strftime("%Y-%m-%d")

            return (
                session.query(EarningsModel)
                .order_by(asc(EarningsModel.time_created))
                .filter(EarningsModel.agent_source_id == agent_id)
                .filter(EarningsModel.time_created.between(interval_start, interval_end))
                .all()
            )
        earnings = (
            session.query(EarningsModel)
            .order_by(asc(EarningsModel.time_created))
            .filter(EarningsModel.agent_source_id == agent_id)
            .filter(EarningsModel.time_created < date_to_check)
            .all()
        )
        return earnings[start:end]

    @staticmethod
    def get_all_for_xlsx():
        earnings_query = (
            session.query(
                EarningsModel.time_created.label('time_created'),
                EarningsModel.summa,
                EarningsModel.comment,
                EarningsModel.currency,
                EarningsModel.source_name,
                LoanAdminsModel.admin_username,
                literal('earnings').label('source'),
            )
            .join(LoanAdminsModel, LoanAdminsModel.id == EarningsModel.agent_source_id)
            .join(SourcesOfIncomeModel, SourcesOfIncomeModel.id == EarningsModel.income_source_id)
        )

        withdraw_query = session.query(
            WithdrawModel.time_created.label('time_created'),
            WithdrawModel.summa * -1,
            null().label('comment'),
            literal(CurrencyEnum.DOLLAR).label('currency'),
            null().label('source_name'),
            LoanAdminsModel.admin_username,
            literal('withdraw').label('source'),
        ).join(LoanAdminsModel, LoanAdminsModel.id == WithdrawModel.agent_source_id)

        query = earnings_query.union(withdraw_query).order_by(desc(text('time_created')))

        return query.all()

    @staticmethod
    def update_earning_from_xlsx(time_created, summa, comment, currency, source_name, admin_username):
        try:
            source_name = source_name if not isinstance(source_name, float) or not math.isnan(
                source_name) else InlineButtonsHelperEnum.OTHER.value

            source = source_of_income_cruds.get_source_by_source_name(source_name)

            comment = comment if not isinstance(comment, float) or not math.isnan(comment) else ''

            currency = CurrencyEnum.UAH if currency == 'UAH' else currency
            new_earnings = EarningsModel(
                time_created=time_created,
                summa=summa,
                comment=comment,
                currency=currency,
                income_source_id=source.id,
                source_name=source_name,
                admin_char=admin_username,
                agent_source_id=agent_cruds.get_by_username(admin_username).id,
                source_percent=source.percent
            )
            new_earnings.id = uuid.uuid4()

            session.add(new_earnings)

            session.commit()
            session.close()

        except Exception as e:
            session.rollback()
            logging.error(e)


earnings_cruds = EarningsCruds()
