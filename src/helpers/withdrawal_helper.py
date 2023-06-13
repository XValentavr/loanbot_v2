import re

from buttons.buttons_back import buttons_back
from buttons.buttons_if_logged_in import buttons_if_logged_in
from commands_handler.agent_balances_handler import get_withdrawal_string
from cruds.agent_cruds import agent_cruds
from cruds.source_of_income_cruds import source_of_income_cruds
from cruds.withdrawal_cruds import withdraw_cruds
from helpers.helper_functions import remove_all_chars, regex_escaper
from helpers.income_and_profit.profit_last_two_weeks_calculator import generate_profit_table
from send_to_owner.send_message_to_owner import send_message_to_owner


def withdrawal_helper(message, loan, agent):
    """
    Button to get prev incomes info
    :param message: chat message
    :param loan: current bot instance
    :return: None
    """
    loan.send_message(message.chat.id,
                      f'{create_withdrawn_for_main_agent(message, loan, agent.admin_username, for_main=False)}\n\nВведите сумму для снятия',
                      parse_mode='MarkdownV2', reply_markup=buttons_back())
    loan.register_next_step_handler(message, lambda msg: withdrawal_next_step(msg, loan, agent))


def withdrawal_next_step(message, loan, agent):
    summa = remove_all_chars(message.text)
    if summa and float(summa) % 100 == 0:
        withdraw_cruds.insert_agent(summa, agent)
        send_message_to_owner(loan=loan, admin=agent.admin_username, instance=None, withdraw=summa)

        buttons_if_logged_in(message, loan)
    else:
        loan.send_message(message.chat.id, 'Сумма неверна, попробуйте ещё раз', reply_to_message_id=message.id,
                          reply_markup=buttons_back())


def create_withdrawn_for_main_agent(message, loan, agent_username, for_main=True):
    agent_to_check = agent_cruds.get_by_username(agent_username)

    all_withdraw = withdraw_cruds.get_all_by_agent_id_and_time(agent=agent_to_check, date_to_check=None)

    profit = source_of_income_cruds.get_source_percent_all_agent_profit_by_limit(agent_username)

    base_profit = generate_profit_table(profit, all_withdraw, for_withdrawal=True, for_main_agent_withdrawal=True)
    if for_main:
        loan.send_message(message.chat.id,
                          generate_withdrawal_for_main_agent_or_not(base_profit, all_withdraw, for_main),
                          reply_to_message_id=message.id,
                          parse_mode='MarkdownV2',
                          reply_markup=buttons_back())
    else:
        return generate_withdrawal_for_main_agent_or_not(base_profit, all_withdraw, for_main)


def generate_withdrawal_for_main_agent_or_not(base_profit, all_withdraw, for_main):
    if base_profit and all_withdraw:
        summa = "\n".join(get_withdrawal_string(all_withdraw))
        final_sum = round(
            float(re.sub(r'\\', '', base_profit)) - float(sum([int(withdraw.summa) for withdraw in all_withdraw])), 2)
        if for_main:
            return f'***Общая сумма дохода: {base_profit}$***\n\nЗапрошено на вывод:\n{summa}\n\nДолг: {regex_escaper(str(final_sum))}$'
        return f'***Общая сумма дохода: {base_profit}$***\n\nЗапрошено на вывод:\n{summa}\n\nДоступно: {regex_escaper(str(final_sum))}$'

    return 'Транзакций пока не найдено'
