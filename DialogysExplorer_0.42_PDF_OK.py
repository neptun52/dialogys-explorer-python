# ============================================================
# Dialogys Explorer 0.3
# Поиск технической документации Renault / Dacia
# ============================================================

import sqlite3
import os
import sys
import textwrap
import json

# ------------------------------------------------------------
# Словарь переводов Dialogys
# ------------------------------------------------------------

DICT_FILE = r"D:\DialogysExplorer\dictionary\dialogys_dictionary.json"


def load_translation_dictionary():

    if not os.path.exists(DICT_FILE):

        print()
        print("Файл словаря не найден:")
        print(DICT_FILE)
        print()

        return {}

    try:

        with open(
            DICT_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception as e:

        print()
        print("Ошибка загрузки словаря:")
        print(e)
        print()

        return {}

# ------------------------------------------------------------
# Поиск французского термина по русскому переводу
# ------------------------------------------------------------

def russian_to_french(search_text, dictionary):

    search_text = search_text.strip().lower()

    if not search_text:
        return None

    sections = (
        "elements",
        "operations",
        "titles"
    )

    for section in sections:

        items = dictionary.get(section, {})

        for french, russian in items.items():

            if not russian:
                continue

            if russian.strip().lower() == search_text:

                return french

    return None

# ------------------------------------------------------------
# Настройка кодировки консоли Windows
# ------------------------------------------------------------

#try:
#    os.system("chcp 65001 > nul")
#except:
#    pass
os.system("chcp 65001 > nul")

DB = "dialogys.db"

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()


# ------------------------------------------------------------
# Основные параметры программы
# ------------------------------------------------------------

PROGRAM_NAME = "Dialogys Explorer"
VERSION = "0.3"

DB = "dialogys.db"

BASE_PATH = r"D:\Program Files1\Dialogys\data\mrnt\fr\d3k"

PDF_FOLDERS = {
    "NT": os.path.join(BASE_PATH, "1-NT"),
    "MR": os.path.join(BASE_PATH, "1-MR"),
}

# ------------------------------------------------------------
# Подключение к базе данных
# ------------------------------------------------------------

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

cur = conn.cursor()
# =================== КОНЕЦ ЧАСТИ 1 ===================
# ============================================================
# Главное меню
# ============================================================

def print_header():

    print("=" * 70)
    print(f"        {PROGRAM_NAME} {VERSION}")
    print("     Поиск технической документации Renault / Dacia")
    print("=" * 70)
    print()


def show_help():

    print("=" * 70)
    print("СПРАВКА")
    print("=" * 70)
    print()

    print("MR - Руководства по ремонту.")
    print("     Инструкции по ремонту,")
    print("     разборке, сборке,")
    print("     регулировкам,")
    print("     моментам затяжки.")

    print()

    print("NT - Технические ноты.")
    print("     Сервисные бюллетени Renault.")
    print("     Специальные технологии ремонта.")
    print("     Рекомендации завода.")

    print()

    input("Нажмите Enter...")


def choose_document_type():

    while True:

        print()
        print("Тип документа:")
        print(" 0 - Выход")
        print(" 1 - NT (Технические ноты)")
        print(" 2 - MR (Руководства по ремонту)")
        print(" 3 - Все документы")
        print(" 4 - Справка")
        print()

        choice = input("Выберите пункт: ").strip()

        if choice == "0":
            return "EXIT"

        elif choice == "1":
            return "NT"

        elif choice == "2":
            return "MR"

        elif choice == "3":
            return None

        elif choice == "4":
            show_help()

        else:
            print()
            print("Неверный выбор.")


# ============================================================
# Поиск документов
# ============================================================

def search_documents(text, doc_filter=None):

    text = text.strip()

    if text == "":
        return []

    # ------------------------------------------------------------
    # Разбиваем запрос на отдельные слова
    # ------------------------------------------------------------

    words = text.split()

    # ------------------------------------------------------------
    # Проверяем минимальную длину
    #
    # Обычные буквенные слова должны иметь минимум 3 символа.
    # Числа и буквенно-цифровые обозначения разрешаем:
    #
    # Scenic 3
    # Clio 2
    # 305
    # H5F
    # K9K
    # ------------------------------------------------------------

    for word in words:

        if word.isalpha() and len(word) < 3:

            print()
            print(
                f"Слово '{word}' слишком короткое."
            )
            print(
                "Для текстовых слов минимум 3 символа."
            )

            return []

    # ------------------------------------------------------------
    # Формируем условия поиска
    #
    # Для каждого слова:
    #
    # (numero LIKE ?
    #  OR titre LIKE ?
    #  OR element_name LIKE ?)
    #
    # Между отдельными словами используется AND.
    # ------------------------------------------------------------

    conditions = []
    params = []

    for word in words:

        conditions.append(
            """
            (
                numero LIKE ?
                OR titre LIKE ?
                OR element_name LIKE ?
            )
            """
        )

        pattern = "%" + word + "%"

        params.extend([
            pattern,
            pattern,
            pattern
        ])

    words_condition = " AND ".join(conditions)

    # ------------------------------------------------------------
    # Все документы
    # ------------------------------------------------------------

    if doc_filter is None:

        sql = f"""
        SELECT DISTINCT
            doc_type,
            numero,
            titre
        FROM documents
        WHERE
            {words_condition}
        ORDER BY numero
        """

    # ------------------------------------------------------------
    # Только NT или MR
    # ------------------------------------------------------------

    else:

        sql = f"""
        SELECT DISTINCT
            doc_type,
            numero,
            titre
        FROM documents
        WHERE
            doc_type = ?
            AND
            {words_condition}
        ORDER BY numero
        """

        params.insert(0, doc_filter)

    
    # ------------------------------------------------------------
    # Выполняем запрос
    # ------------------------------------------------------------

    cur.execute(
        sql,
        tuple(params)
    )

    return cur.fetchall()

# ============================================================
# ЧАСТЬ 4.2
# Главный цикл программы
# ============================================================
# ============================================================
# Просмотр результатов поиска
# ============================================================

def browse_results(rows):

    offset = 0
    page_size = 20

    while True:

        selected_rows = rows[offset:offset + page_size]

        if not selected_rows:
            print("\nБольше документов нет.")
            offset = 0
            continue

        print()
        print("=" * 70)
        print("                    РЕЗУЛЬТАТЫ ПОИСКА")
        print("=" * 70)
        print()

        print(f"Найдено документов : {len(rows)}")

        start = offset + 1
        end = min(offset + page_size, len(rows))

        print(f"Показано           : {start} - {end}")
        print()

        print("-" * 90)
        print("№   База  Документ            Описание")
        print("-" * 90)

        for i, row in enumerate(selected_rows, start=1):

            title_lines = textwrap.wrap(row["titre"], width=55)

            print(
                f"{i:2}. "
                f"{row['doc_type']:2}   "
                f"{row['numero']:<12} "
                f"{title_lines[0]}"
            )

            for line in title_lines[1:]:
                print(" " * 20 + line)

        print()
        print("Enter - следующие 20")
        print("U     - предыдущие 20")
        print("0     - новый поиск")
        print("1-20  - выбрать документ")

        choice = input("\nВаш выбор: ").strip().upper()

        if choice == "":
            offset += page_size
            continue

        if choice == "U":

            offset -= page_size

            if offset < 0:
                offset = 0

            continue

        if choice == "0":
            return None 

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(selected_rows):
                return selected_rows[number - 1]

        print("Неверный выбор.")# конец вставки
# ============================================================
# Получение разделов документа
# ============================================================

def get_document_elements(doc_type, numero):

    sql = """
    SELECT DISTINCT
        element_name
    FROM documents
    WHERE
        doc_type = ?
        AND numero = ?
    ORDER BY element_name
    """

    cur.execute(sql, (doc_type, numero))

    return cur.fetchall()

# ============================================================
# Просмотр разделов документа
# ============================================================

def browse_elements(elements):

    print()
    print("Разделы документа")
    print("-" * 70)

    for i, row in enumerate(elements, start=1):
        print(f"{i:2}. {row['element_name']}")
        
    print()
    print("0 - Назад")

    while True:

        choice = input("Выберите раздел: ").strip()

        if choice == "0":
            return None

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(elements):
                return elements[number - 1]

        print("Неверный выбор.")
# ============================================================
# Получение полной информации о разделе
# ============================================================

def get_element_info(doc_type, numero, element_name):

    sql = """
    SELECT *
    FROM documents
    WHERE
        doc_type = ?
        AND numero = ?
        AND element_name = ?
    LIMIT 1
    """

    cur.execute(sql, (doc_type, numero, element_name))

    return cur.fetchone()
# ------------------------------------------------------------
# Поиск PDF
# ------------------------------------------------------------

def find_pdf(numero):

    found = []

    numero = numero.upper()
    # убираем последнюю букву модификации
    import re

    m = re.search(r"\d+", numero)

    if m:
        base_numero = m.group()
    else:
        base_numero = numero

    for folder in PDF_FOLDERS.values():

        for root, dirs, files in os.walk(folder):

            for file in files:

                if not file.lower().endswith(".pdf"):
                    continue

                if base_numero in file.upper():

                    full_path = os.path.join(root, file)

                    found.append(full_path)

    return found

# ------------------------------------------------------------
# Открытие PDF
# ------------------------------------------------------------

def open_pdf(numero):
    numero = numero.strip().upper()

    files = find_pdf(numero)

    if not files:
        print("\nДокумент не найден.")
        return

    if len(files) == 1:

        os.startfile(files[0])
        return

    print()
    print("Найдено несколько документов:")
    print()

    for i, file in enumerate(files, start=1):
        print(f"{i}. {os.path.basename(file)}")

    while True:

        choice = input("\nВыберите номер файла (0 - отмена): ").strip()

        if choice == "0":
            return

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(files):

                os.startfile(files[number - 1])
                return

        print("Неверный выбор.")

# ================================================
#          главная 
# ================================================

def main():


#   print("=== ТЕСТ: ЗАПУЩЕН НОВЫЙ MAIN ===")

    translation_dictionary = load_translation_dictionary()

    while True:

        # os.system("cls")

        print_header()

        doc_filter = choose_document_type()

        if doc_filter == "EXIT":
            break

        print()

        text = input("Что искать: ").strip()

        if text == "0":
            break

        if text == "":
            continue
        
        # ------------------------------------------------------------
        # Проверяем, является ли запрос русским переводом
        # ------------------------------------------------------------

        french_query = russian_to_french(
            text,
            translation_dictionary
        )

        if french_query:

            print()
            print("Русский запрос:", text)
            print("Найден французский термин:", french_query)

            search_text = french_query

        else:

            search_text = text

# ------------------------------------------------------------
# Поиск документов
# ------------------------------------------------------------
        print()
        print("=== ДИАГНОСТИКА ПОИСКА ===")
        print("Исходный запрос :", text)
        print("Запрос для поиска:", search_text)
        print("Тип документа   :", doc_filter)
        print("==========================")
        rows = search_documents(search_text, doc_filter)

        print()

        if len(rows) == 0:

            print("Ничего не найдено.")
            input("\nНажмите Enter...")
            continue

        print(f"Найдено документов: {len(rows)}")

        selected = browse_results(rows)

        if selected is None:
            continue
        print()
        print(f"Документ: {selected['doc_type']}  {selected['numero']}")
        elements = get_document_elements(
            selected["doc_type"],
            selected["numero"]
        )

        element = browse_elements(elements)

        if element is None:
            continue
        info = get_element_info(
            selected["doc_type"],
            selected["numero"],
            element["element_name"]
        )

        print()
        print("=" * 70)
        print("Все поля записи")
        print("=" * 70)
        print("Ищем PDF:", selected["numero"])

        for key in info.keys():
            print(f"{key:20} : {info[key]}")

        # Открытие PDF только один раз
        open_pdf(selected["numero"])  # открытие pdf
        input("\nНажмите Enter...")


if __name__ == "__main__":
    main()