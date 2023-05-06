from cruds.source_of_income_cruds import source_of_income_cruds


def fill_source():
    data = {
        'Шест': 5,
        'Крюк': 10,
        'Антон': 3,
        'Искусство': 15,
        'Лойер': 20,
        'Британия': 10,
        'Армянин': 5,
        'Парашют': 20,
        'Гонщик': 5,
        'Швейцарец': 30,
        'Новострой': 12,
        'Руда': 20,
        'Ювелир': 10,
        'Агро (Ирина Ии)': 10,
        'БМВ': 5,
        'Кум': 30,
        'Чин': 10,
        'Фунт': 30,
        'Депутат': 2,
        'Турист': 5,
        'Ребёнок': 20,
        'Цыган': 5,
        'Готель': 1
    }
    for key in data.keys():
        source_of_income_cruds.insert_source(key, data[key])


if __name__ == "__main__":
    print("___starting script___")
    fill_source()
    print("Success!")
