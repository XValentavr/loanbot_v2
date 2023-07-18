import calendar
from typing import Dict

from buttons.buttons_back import buttons_back
from buttons.buttons_if_logged_in import buttons_if_logged_in
from buttons.buttons_main_agent import buttons_main_agents_commands
from commands_handler.agent_balances_handler import get_agents_balance, get_more_history
from commands_handler.base_data_expense_or_earnings_handler import ready_event, change_event
from buttons.buttons_insert_data import buttons_insert_data
from buttons.buttons_my_prev_incomes import buttons_get_previous_incomes
from commands_handler.earning_data_handler import (
    earnings_data_handler,
    earnings_insert_data_handler,
    earnings_with_other_source_insert_data_handler,
)
from commands_handler.expense_data_handler import expense_data_handler
from commands_handler.show_balance_handler import get_agent_balance, get_more_agent_balance
from cruds.agent_cruds import agent_cruds
from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.date.date import get_current_month, get_prev_month
from helpers.enums.helper_main_agent_enum import HelperMainAgentEnum
from helpers.enums.inline_buttons_enum import InlineButtonsEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum
from helpers.income_and_profit.profit_other_date_calculator import get_profit_of_other_dates
from helpers.withdrawal_helper import withdrawal_helper, create_withdrawn_for_main_agent

month, year = get_current_month()
agent_set_income_source: Dict = {}
has_expense: Dict = {}
current_month_year: Dict = {'month': month, 'year': year}
main_agent_get_info_about: Dict = {}


def event_main_buttons_helper(call, agent, loan):
    if call.data == InlineButtonsEnum.BALANCE:
        get_agent_balance(message=call.message, loan=loan, agent=agent)

    elif call.data == InlineButtonsEnum.WITHDRAWAL:
        withdrawal_helper(message=call.message, loan=loan, agent=agent)

    elif call.data == InlineButtonsEnum.BACK:
        buttons_if_logged_in(call.message, loan)

    elif call.data == InlineButtonsEnum.INCOME:
        loan.clear_step_handler_by_chat_id(call.message.chat.id)

        buttons_get_previous_incomes(message=call.message, loan=loan, agent=agent)

    elif call.data == InlineButtonsEnum.INSERT:
        loan.clear_step_handler_by_chat_id(call.message.chat.id)

        buttons_insert_data(call.message, loan)

    elif call.data == InlineButtonsEnum.EXPENSE:
        has_expense[agent.admin_username] = True

        expense_data_handler(message=call.message, loan=loan)

    elif call.data == InlineButtonsEnum.EARNINGS:
        if has_expense:
            del has_expense[agent.admin_username]

        earnings_data_handler(message=call.message, loan=loan)

    else:
        event_other_buttons_helper(call, agent, loan)


def event_other_buttons_helper(call, agent, loan):
    income_sources = [source.source for source in source_of_income_cruds.get_all_sources()]

    if call.data == InlineButtonsHelperEnum.READY:
        expense = False

        if has_expense.get(agent.admin_username):
            expense = True
            del has_expense[agent.admin_username]

        ready_event(message=call.message, agent=agent, loan=loan, expense=expense,
                    source=agent_set_income_source.get(agent.admin_username))

    elif call.data == InlineButtonsHelperEnum.CHANGE:
        change_event(message=call.message, loan=loan)

    elif call.data == InlineButtonsEnum.PREV_INCOMES:
        loan.send_message(
            chat_id=call.message.chat.id, text=get_profit_of_other_dates(agent), parse_mode='MarkdownV2',
            reply_markup=buttons_back()
        )

    elif call.data in income_sources and call.data != InlineButtonsHelperEnum.OTHER:
        source = source_of_income_cruds.get_source_by_source_name(call.data)

        agent_set_income_source[agent.admin_username] = source

        earnings_insert_data_handler(message=call.message, loan=loan)

    elif call.data in income_sources and call.data == InlineButtonsHelperEnum.OTHER:
        agent_set_income_source[agent.admin_username] = call.message.text

        earnings_with_other_source_insert_data_handler(message=call.message, loan=loan)

    else:
        main_agent_command_helper(call, loan, agent)


def main_agent_command_helper(call, loan, agent):
    all_agents = [agent.admin_username for agent in agent_cruds.get_all_agents()]
    if call.data in all_agents:
        mnth, _ = get_current_month()
        current_month_year['month'] = mnth
        buttons_main_agents_commands(call.message, loan)
        main_agent_get_info_about[agent.admin_username] = call.data

    elif call.data == HelperMainAgentEnum.MAIN_AGENT_HISTORY:
        mnth, _ = get_current_month()

        current_month_year['month'] = mnth
        get_agents_balance(message=call.message, loan=loan,
                           agent_username=main_agent_get_info_about[agent.admin_username])
    elif call.data == HelperMainAgentEnum.MAIN_AGENT_WITHDRAW:
        mnth, _ = get_current_month()

        current_month_year['month'] = mnth
        create_withdrawn_for_main_agent(call.message, loan,
                                        agent_username=main_agent_get_info_about[agent.admin_username])
    elif call.data == HelperMainAgentEnum.MORE_HISTORY:
        prev_month = get_prev_month(current_month_year['month'])
        current_month_year['month'] = calendar.month_name[prev_month]
        get_more_history(
            message=call.message,
            loan=loan,
            agent_username=main_agent_get_info_about[agent.admin_username],
            current_month_year=current_month_year,
        )

    elif call.data == HelperMainAgentEnum.MORE_BALANCE:
        get_more_agent_balance(call.message, loan, agent)
