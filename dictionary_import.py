import json
import os
import pyperclip


# ------------------------------------------------------------
# Настройки
# ------------------------------------------------------------

VERSION = "1.0"

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
# Проверка буфера
# ------------------------------------------------------------

def read_clipboard():

    print()
    print("=" * 60)
    print("DIALOGYS DICTIONARY IMPORT")
    print("Версия:", VERSION)
    print("=" * 60)

    print()
    print("Скопируйте блок переводов в буфер обмена.")
    input("После этого нажмите Enter...")

    text = pyperclip.paste()

    return text


# ------------------------------------------------------------
# Предварительный просмотр
# ------------------------------------------------------------

def preview(text):

    print()
    print("=" * 60)
    print("ПРОСМОТР БУФЕРА ОБМЕНА")
    print("=" * 60)

    lines = text.splitlines()

    print()
    print("Найдено строк:", len(lines))
    print()

    for i, line in enumerate(lines, 1):

        if line.strip():

            print(f"{i}. {line}")


    print()
    print("=" * 60)
    print("1 - начать импорт")
    print("0 - отменить")
    print("=" * 60)


    choice = input("Выбор: ").strip()

    return choice == "1"

# ------------------------------------------------------------
# Обработка переводов в памяти
# ------------------------------------------------------------

def process_translation(text, dictionary):

    print()
    print("=" * 60)
    print("ОБРАБОТКА ПЕРЕВОДОВ")
    print("=" * 60)

    lines = text.splitlines()

    updated = 0
    not_found = []

    # делаем копию словаря
    temp_dictionary = json.loads(
        json.dumps(dictionary, ensure_ascii=False)
    )


    for line in lines:

        line = line.strip()

        if not line:
            continue


        if "=" not in line:

            print("Пропущено:", line)
            continue


        french, russian = line.split("=", 1)

        french = french.strip()
        russian = russian.strip()


        found = False


        for section in (
            "elements",
            "operations",
            "titles"
        ):


            if french in temp_dictionary[section]:

                temp_dictionary[section][french] = russian


                print(
                    f"OK [{section}] {french} -> {russian}"
                )


                updated += 1
                found = True
                break



        if not found:

            print(
                "НЕ НАЙДЕНО:",
                french
            )

            not_found.append(french)



    print()
    print("=" * 60)
    print("РЕЗУЛЬТАТ")
    print("=" * 60)

    print(
        "Прочитано строк:",
        len(lines)
    )

    print(
        "Обновлено:",
        updated
    )

    print(
        "Не найдено:",
        len(not_found)
    )
###
    print()
    print("Изменения пока только в памяти.")
    print("JSON файл не изменён.")


    if not_found:

        print()
        print("=" * 60)
        print("НЕ НАЙДЕННЫЕ ТЕРМИНЫ")
        print("=" * 60)

        for i, item in enumerate(not_found, 1):

            print(
                f"{i}. {item}"
            )


    return temp_dictionary
###

# ------------------------------------------------------------
# Главная программа
# ------------------------------------------------------------

def main():

    if not os.path.exists(DICT_FILE):

        print("Файл словаря не найден:")
        print(DICT_FILE)
        input("\nEnter...")
        return


    dictionary = load_dictionary()


    text = read_clipboard()

###
    if not preview(text):

        print()
        print("Импорт отменён.")
        input("\nEnter...")
        return


    temp_dictionary = process_translation(
        text,
        dictionary
)
    print()
    print("=" * 60)
    print("СОХРАНИТЬ ИЗМЕНЕНИЯ?")
    print("=" * 60)

    print()
    print("1 - сохранить в JSON")
    print("0 - отменить изменения")


    choice = input("\nВыбор: ").strip()


    if choice == "1":

        with open(
            DICT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                temp_dictionary,
                f,
                indent=4,
                ensure_ascii=False
            )

        print()
        print("Словарь успешно сохранён.")


    else:

        print()
        print("Изменения отменены.")
        print("JSON файл не изменён.")


    input("\nEnter...")

print()
print("Основной словарь пока не изменён.")


input("\nEnter...")
###

# ------------------------------------------------------------

if __name__ == "__main__":

    main()