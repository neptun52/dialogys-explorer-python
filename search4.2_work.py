# ============================================================
# Dialogys Explorer 0.3
# Поиск технической документации Renault / Dacia
# ============================================================

import sqlite3
import os
import sys
import textwrap

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

# ===== ВРЕМЕННАЯ ПРОВЕРКА СТРУКТУРЫ БАЗЫ 1=====
#print("\nПервые 10 записей базы:\n")

#cur.execute("""
#SELECT doc_type, numero, titre
#FROM documents
#LIMIT 10
#""")

#for row in cur.fetchall():
#    print(row["doc_type"], row["numero"], row["titre"])

#input("\nНажмите Enter...")
# ===== КОНЕЦ ВРЕМЕННОЙ ПРОВЕРКИ 1=====

# ===== ВРЕМЕННАЯ ПРОВЕРКА СТРУКТУРЫ БАЗЫ =====
#for row in cur.execute("PRAGMA table_info(documents)"):
#    print(row)
# ===== КОНЕЦ ВРЕМЕННОЙ ПРОВЕРКИ =====

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

    if doc_filter is None:

        sql = """
        SELECT DISTINCT 
            doc_type,
            numero,
            titre
        FROM documents
        WHERE
            numero LIKE ?
            OR titre LIKE ?
            OR element_name LIKE ?
        ORDER BY numero
        """

        params = (
            "%" + text + "%",
            "%" + text + "%",
            "%" + text + "%"
            
        )

    else:

        sql = """
        SELECT DISTINCT
            doc_type,
            numero,
            titre
        FROM documents
        WHERE
            doc_type = ?
            AND
            (
                numero LIKE ?
                OR titre LIKE ?
                OR element_name LIKE ?
            )
        ORDER BY numero
        """

        params = (
            doc_filter,
            "%" + text + "%",
            "%" + text + "%",
            "%" + text + "%"
        )

    cur.execute(sql, params)

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
        print("№   База Документ      Описание")
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
        print("0 - новый поиск")

        choice = input("Выберите документ: ").strip()

        if choice == "":
            offset += page_size
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

    base_numero = re.match(r"\d+", numero).group()

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

    while True:

        # os.system("cls")

        print_header()

        doc_filter = choose_document_type()

        if doc_filter == "EXIT":
            break

        print()

        text = input("Что искать: ").strip()

        if text == "":
            continue

        rows = search_documents(text, doc_filter)

        print()

        if len(rows) == 0:

            print("Ничего не найдено.")
            input("\nНажмите Enter...")
            continue

        print(f"Найдено документов: {len(rows)}")

        selected = browse_results(rows)

        if selected is None:
            continue

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

            open_pdf(selected["numero"])  # открытие pdf
        input("\nНажмите Enter...")


if __name__ == "__main__":
    main()