import json
import os


# ------------------------------------------------------------
# Настройки
# ------------------------------------------------------------

DICT_FILE = r"D:\DialogysExplorer\dictionary\dialogys_dictionary.json"


# ------------------------------------------------------------
# Загрузка словаря
# ------------------------------------------------------------

def load_dictionary():

    with open(
        DICT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


# ------------------------------------------------------------
# Сохранение словаря
# ------------------------------------------------------------

def save_dictionary(dictionary):

    with open(
        DICT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dictionary,
            f,
            indent=4,
            ensure_ascii=False
        )


# ------------------------------------------------------------
# Редактирование раздела
# ------------------------------------------------------------

def translate_section(dictionary, section):

    items = dictionary[section]

    print()
    print("=" * 70)
    print("Раздел:", section)
    print("Всего записей:", len(items))
    print("=" * 70)


    count = 0

    for french in items:

        russian = items[french]


        # уже переведенные пропускаем
        if russian != "":

            continue


        print()
        print("Французский:")
        print(french)

        print()

        answer = input(
            "Русский перевод (Enter - пропустить, 0 - выход): "
        ).strip()


        if answer == "0":

            save_dictionary(dictionary)

            print("Словарь сохранён.")

            return


        if answer != "":

            items[french] = answer

            save_dictionary(dictionary)

            count += 1

            print("Сохранено.")


    print()
    print("Новых переводов добавлено:", count)


# ------------------------------------------------------------
# Главное меню
# ------------------------------------------------------------

def main():

    if not os.path.exists(DICT_FILE):

        print("Файл словаря не найден:")
        print(DICT_FILE)
        return


    dictionary = load_dictionary()


    while True:

        print()
        print("=" * 70)
        print("DIALOGYS TRANSLATE DICTIONARY")
        print("=" * 70)

        print()
        print("1 - Элементы")
        print("2 - Операции")
        print("3 - Документы")
        print("0 - Выход")


        choice = input("\nВыбор: ").strip()


        if choice == "1":

            translate_section(
                dictionary,
                "elements"
            )


        elif choice == "2":

            translate_section(
                dictionary,
                "operations"
            )


        elif choice == "3":

            translate_section(
                dictionary,
                "titles"
            )


        elif choice == "0":

            save_dictionary(dictionary)

            print("Выход.")
            break


        else:

            print("Неверный выбор.")



# ------------------------------------------------------------

if __name__ == "__main__":

    main()