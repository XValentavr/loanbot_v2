from commands_handler.base_data_expense_or_earnings_handler import ready_event, change_event
from buttons.buttons_insert_data import buttons_insert_data
from buttons.buttons_my_prev_incomes import buttons_get_previous_incomes
from commands_handler.earning_data_handler import earnings_data_handler, earnings_insert_data_handler, \
    earnings_with_other_source_insert_data_handler
from commands_handler.expense_data_handler import expense_data_handler
from commands_handler.show_balance_handler import get_agent_balance
from cruds.source_of_income_cruds import source_of_income_cruds
from helpers.enums.inline_buttons_enum import InlineButtonsEnum
from helpers.enums.inline_buttons_helper_enum import InlineButtonsHelperEnum

agent_set_income_source = {}


def event_main_buttons_helper(call, agent, loan):
    if call.data == InlineButtonsEnum.BALANCE:
        get_agent_balance(agent)

    elif call.data == InlineButtonsEnum.INCOME:
        buttons_get_previous_incomes(message=call.message, loan=loan)

    elif call.data == InlineButtonsEnum.INSERT:
        buttons_insert_data(call.message, loan)

    elif call.data == InlineButtonsEnum.EXPENSE:
        expense_data_handler(message=call.message, loan=loan)

    elif call.data == InlineButtonsEnum.EARNINGS:
        earnings_data_handler(message=call.message, loan=loan)

    else:
        event_other_buttons_helper(call, agent, loan)


def event_other_buttons_helper(call, agent, loan):
    income_sources = [source.source for source in source_of_income_cruds.get_all_sources()]

    if call.data == InlineButtonsHelperEnum.READY:

        ready_event(message=call.message,
                    username=call.from_user.username,
                    agent=agent,
                    loan=loan,
                    source=agent_set_income_source.get(call.from_user.username))

    elif call.data == InlineButtonsHelperEnum.CHANGE:
        change_event(message=call.message, loan=loan)

    elif call.data in income_sources and call.data != InlineButtonsHelperEnum.OTHER:
        source = source_of_income_cruds.get_source_by_source_name(call.data)

        agent_set_income_source[call.from_user.username] = source

        earnings_insert_data_handler(message=call.message, loan=loan)

    elif call.data in income_sources and call.data == InlineButtonsHelperEnum.OTHER:

        agent_set_income_source[call.from_user.username] = call.message.text

        earnings_with_other_source_insert_data_handler(message=call.message, loan=loan)
