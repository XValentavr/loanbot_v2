from cruds.source_of_income_cruds import source_of_income_cruds


def fill_source():
    list_of_sources = ['Шест', 'Крюк', 'Антон', 'Искусство', 'Лойер', 'Британия', 'Армянин', 'Парашют', 'Гонщик',
                       'Швейцарец',
                       'Новострой', 'Руда', 'Ювелир', 'Агро (Ирина Ии)', 'БМВ', 'Кум', 'Чин', 'Фунт', 'Депутат',
                       'Турист',
                       'Ребёнок', 'Цыган', 'Готель', 'Другое']

    for source in list_of_sources:
        source_of_income_cruds.insert_source(source)


if __name__ == "__main__":
    print("___starting script___")
    fill_source()
    print("Success!")
