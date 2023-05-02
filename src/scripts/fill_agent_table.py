from cruds.agent_cruds import agent_cruds
from helpers.encrypt_and_decrypt import encryptor


def fill_agent_table():
    user_password = {'Valentavr': '12345',
                     'demkov': '11111'}
    for key in user_password.keys():
        password = encryptor.generate_encrypted_password(characters=user_password.get(key))
        agent_cruds.insert_agent_cruds(username=key, password=password, is_logged_in=False)


if __name__ == '__main__':
    print('___ starting script ___')
    fill_agent_table()
