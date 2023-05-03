from buttons.button_ready_or_not import buttons_ready_or_not
from buttons.buttons_if_logged_in import buttons_if_logged_in
from cruds.earning_cruds import earnings_cruds

other_source = {}


def base_data_handler(message, loan):
    other_source[message.from_user.username] = message.text

    loan.send_message(message.chat.id, "Внесите сумму и комментарий")
    loan.register_next_step_handler(message, lambda msg: check_summa_and_comment(msg, loan))


def check_summa_and_comment(message, loan):
    buttons_ready_or_not(message, loan)


def ready_event(message, agent, loan, source, username):
    try:
        earnings_cruds.insert_source(summa=message.text, comment=message.text,
                                     source_id=source.id if not other_source.get(username) else None,
                                     agent_id=agent.id,
                                     is_other_source=other_source.get(username) if other_source.get(username) else None)

        loan.send_message(message.chat.id, "Транзакция успешная!")
    except Exception:
        loan.send_message(message.chat.id, "Что-то пошло не так, попробуйте ещё раз")

    buttons_if_logged_in(message, loan)


def change_event(message, loan):
    base_data_handler(message, loan)
