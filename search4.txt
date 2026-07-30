# ============================================================
# Dialogys Explorer 0.3
# Поиск технической документации Renault / Dacia
# ============================================================

import sqlite3
import os
import sys

# ------------------------------------------------------------
# Настройка кодировки консоли Windows
# ------------------------------------------------------------

try:
    os.system("chcp 65001 > nul")
except:
    pass

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
        SELECT
            doc_type,
            numero,
            titre,
            element_name
        FROM documents
        WHERE
            titre LIKE ?
            OR element_name LIKE ?
        ORDER BY numero
        """

        params = (
            "%" + text + "%",
            "%" + text + "%"
        )

    else:

        sql = """
        SELECT
            doc_type,
            numero,
            titre,
            element_name
        FROM documents
        WHERE
            doc_type = ?
            AND
            (
                titre LIKE ?
                OR element_name LIKE ?
            )
        ORDER BY numero
        """

        params = (
            doc_filter,
            "%" + text + "%",
            "%" + text + "%"
        )

    cur.execute(sql, params)

    return cur.fetchall()
# =================== КОНЕЦ ЧАСТИ 3 ===================
