import requests

from helpers.creds import Creds


def get_actual_currency():
    url = Creds.CURRENCY_URL
    params = {
        'app_id': Creds.CURRENCY_API_ID
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        uah_rate = round(data['rates']['UAH'], 1)
        eur_rate = round(data['rates']['EUR'], 1)
        return uah_rate, eur_rate
    else:
        return '', ''