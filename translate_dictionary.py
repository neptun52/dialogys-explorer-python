import json
import os
import pyperclip



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
# Просмотр терминов для перевода с переходом страниц
# ------------------------------------------------------------

def show_translation_batch(dictionary, section):

    items = dictionary[section]

    # собираем только не переведённые термины
    terms = []

    for french, russian in items.items():

        if russian == "":
            terms.append(french)


    if len(terms) == 0:

        print()
        print("Все термины этого раздела уже переведены.")
        return


    print()
    print("=" * 70)
    print("Раздел:", section)
    print("Всего не переведено:", len(terms))
    print("=" * 70)


    start = input(
        "\nС какого номера начать? (Enter - с начала): "
    ).strip()


    if start == "":
        position = 0

    elif start.isdigit():

        position = int(start) - 1

        if position < 0:
            position = 0

    else:

        position = 0



    while True:

        batch = terms[position:position + 20]


        if not batch:

            print()
            print("Больше терминов нет.")
            break


        print()
        print("-" * 70)

        for i, term in enumerate(
                batch,
                start=position + 1):

            print(f"{i}. {term}")


        print("-" * 70)


        # копирование в буфер
        import pyperclip

        pyperclip.copy(
            "\n".join(batch)
        )


        print()
        print(
            "Эти 20 терминов скопированы в буфер."
        )


        print()
        print("Enter - следующие 20")
        print("1 - вставить готовый перевод")
        print("0 - выход")


        choice = input(
            "Выбор: "
        ).strip()

        if choice == "1":

            import_translation_block(dictionary)

            # После импорта заново собираем
            # список ещё не переведённых терминов

            terms = []

            for french, russian in dictionary[section].items():

                if russian == "":
                    terms.append(french)

            # Если все термины переведены

            if not terms:

                print()
                print("Все термины этого раздела уже переведены.")
                break

            # Возвращаемся к текущей позиции
            continue
        if choice == "0":

            break


        if choice == "":

            position += 20

        elif choice.isdigit():

            position = int(choice) - 1

        else:

            print("Неверный ввод.")


# ------------------------------------------------------------
# Добавление готовых переводов
# ------------------------------------------------------------
def process_translation(text, dictionary):
    print(">>> ВОШЛИ В process_translation()") ### потом удалить
    print()
    print("=" * 70)
    print("ОБРАБОТКА ПЕРЕВОДОВ В ПАМЯТИ")
    print("=" * 70)

    lines = text.splitlines()

    updated = 0
    not_found = []

    # Копия словаря.
    # Основной JSON пока не изменяется.
    temp_dictionary = json.loads(
        json.dumps(
            dictionary,
            ensure_ascii=False
        )
    )

    sections = [
        "elements",
        "operations",
        "titles"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if "=" not in line:
            continue

        french, russian = line.split("=", 1)

        french = french.strip()
        russian = russian.strip()

        if not french or not russian:
            continue

        found = False

        for section in sections:

            if french in temp_dictionary[section]:

                old_translation = (
                    temp_dictionary[section][french]
                )

                print()
                print("-" * 70)
                print("ФРАНЦУЗСКИЙ:")
                print(french)

                print()
                print("СТАРЫЙ ПЕРЕВОД:")
                print(
                    old_translation
                    if old_translation
                    else "(перевода пока нет)"
                )

                print()
                print("НОВЫЙ ПЕРЕВОД:")
                print(russian)

                print()

                answer = input(
                    "Enter - принять новый перевод\n"
                    "S - свой перевод\n"
                    "0 - отменить весь импорт\n"
                    "Выбор: "
                ).strip()

                if answer == "0":
                    print()
                    print("Импорт отменён.")
                    return None

                if answer.lower() in ("s", "ы"):

                    custom = input(
                        "Введите свой перевод: "
                    ).strip()

                    if custom:
                        russian = custom
                    else:
                        print(
                            "Пустой перевод. "
                            "Оставлен новый перевод."
                        )

                temp_dictionary[section][french] = russian

                print()
                print(
                    f"OK [{section}]"
                )
                print(
                    f"Сохранено в памяти: {russian}"
                )

                updated += 1
                found = True
                break

        if not found:

            print()
            print("НЕ НАЙДЕНО:", french)

            not_found.append(french)

    print()
    print("=" * 70)
    print("РЕЗУЛЬТАТ")
    print("=" * 70)

    print("Прочитано строк:", len(lines))
    print("Обновлено:", updated)
    print("Не найдено:", len(not_found))

    print()
    print("Изменения пока только в памяти.")
    print("JSON файл не изменён.")

    return temp_dictionary
# ------------------------------------------------------------
# Сщхранение резервной копии файла JSON
# ------------------------------------------------------------
def backup_dictionary():

    backup_file = DICT_FILE + ".backup"

    try:

        with open(
            DICT_FILE,
            "r",
            encoding="utf-8"
        ) as source:

            data = source.read()

        with open(
            backup_file,
            "w",
            encoding="utf-8"
        ) as backup:

            backup.write(data)

        print()
        print("=" * 70)
        print("РЕЗЕРВНАЯ КОПИЯ СОЗДАНА")
        print("=" * 70)

        print()
        print("Файл:")
        print(backup_file)

        return True

    except Exception as error:

        print()
        print("=" * 70)
        print("ОШИБКА СОЗДАНИЯ РЕЗЕРВНОЙ КОПИИ")
        print("=" * 70)

        print()
        print(error)

        return False
# ------------------------------------------------------------
# Импорт готовых переводов из буфера обмена
# ------------------------------------------------------------
####
def import_translation_block(dictionary):

    print()
    print("=" * 70)
    print("ИМПОРТ ПЕРЕВОДОВ ИЗ БУФЕРА ОБМЕНА")
    print("=" * 70)

    # Читаем ТЕКУЩЕЕ содержимое буфера
    text = pyperclip.paste()

    if not text.strip():

        print()
        print("Буфер обмена пуст.")
        input("\nНажмите Enter...")
        return

    lines = text.splitlines()

    translation_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if "=" not in line:
            continue

        french, russian = line.split("=", 1)

        french = french.strip()
        russian = russian.strip()

        if french and russian:

            translation_lines.append(
                (french, russian)
            )

    if not translation_lines:

        print()
        print("В буфере не найдено переводов")
        print("в формате:")
        print("французский = русский")

        input("\nНажмите Enter...")
        return

    print()
    print("Найдено переводов:",
          len(translation_lines))

    print()

    for i, (french, russian) in enumerate(
            translation_lines, 1):

        print(
            f"{i}. {french} = {russian}"
        )

    print()
    print("=" * 70)
    print("1 - начать обработку")
    print("0 - отменить")
    print("=" * 70)

    choice = input("\nВыбор: ").strip()

    if choice != "1":

        print()
        print("Импорт отменён.")

        input("\nНажмите Enter...")
        return

    # --------------------------------------------------------
    # Теперь передаём блок в нашу безопасную обработку
    # --------------------------------------------------------

    translation_text = "\n".join(
        f"{french} = {russian}"
        for french, russian
        in translation_lines
    )

    temp_dictionary = process_translation(
        translation_text,
        dictionary
    )

    # Пользователь отменил обработку
    if temp_dictionary is None:

        print()
        print("Изменения отменены.")

        input("\nНажмите Enter...")
        return

    # --------------------------------------------------------
    # Спрашиваем, сохранять ли изменения
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("СОХРАНЕНИЕ ИЗМЕНЕНИЙ")
    print("=" * 70)

    print()
    print("1 - сохранить в JSON")
    print("0 - отменить изменения")

    save_choice = input(
        "\nВыбор: "
    ).strip()

    if save_choice == "1":

        if not backup_dictionary():

            print()
            print(
                "Резервная копия не создана."
            )

            print(
                "JSON файл НЕ изменён."
            )

            input("\nНажмите Enter...")
            return

        save_dictionary(
            temp_dictionary
        )

        # Обновляем основной словарь
        dictionary.clear()
        dictionary.update(
            temp_dictionary
        )

        print()
        print("Словарь успешно сохранён.")

    else:

        print()
        print("Изменения отменены.")

    input("\nНажмите Enter...")

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
#####


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
        print("1 - Элементы (20)")
        print("2 - Операции (20)")
        print("3 - Документы (20)")
        print("4 - Добавить готовые переводы")
        print("0 - Выход")


        choice = input("\nВыбор: ").strip()


        if choice == "1":

            show_translation_batch(
                dictionary,
                "elements"
            )


        elif choice == "2":

            show_translation_batch(
                dictionary,
                "operations"
            )


        elif choice == "3":

            show_translation_batch(
                dictionary,
                "titles"
            )
        elif choice == "4":

            import_translation_block(dictionary)
                 
            continue

        elif choice == "0":

            save_dictionary(dictionary)

            print("Выход.")
            break


        else:

            print("Неверный выбор.")



# ------------------------------------------------------------

if __name__ == "__main__":

    main()
###########  test   
#    dictionary = load_dictionary()

#  import_translation_block(dictionary)
############ test end