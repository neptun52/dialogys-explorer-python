import sqlite3
import os
import sys

os.system("chcp 65001 > nul")

DB = "dialogys.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()
# ============================================================
# НАЧАЛО ВСТАВКИ №1
# Настройки программы
# ============================================================

BASE_PATH = r"D:\Program Files1\Dialogys\data\mrnt\fr\d3k"

PDF_FOLDERS = {
    "NT": os.path.join(BASE_PATH, "1-NT"),
    "MR": os.path.join(BASE_PATH, "1-MR"),
}

PROGRAM_NAME = "Dialogys Explorer"
VERSION = "0.2"

# ============================================================
# КОНЕЦ ВСТАВКИ №1
# ============================================================
# ============================================================
# НАЧАЛО ВСТАВКИ №1
# Настройки программы
# ============================================================

print("=" * 70)
print("        Dialogys Explorer 0.3")
print("     Поиск технической документации Renault")
print("=" * 70)

print()
print("Тип документа:")
print(" 0 - Выход")
print(" 1 - NT  (Технические ноты, сервисные бюллетени)")
print(" 2 - MR  (Руководства по ремонту)")
print(" 3 - Все документы")
print(" 4 - Справка")
print()
doc_filter = input("Выберите тип документа (0-4): ").strip()
# ==========================================================
# Выход из программы
# ==========================================================

if doc_filter == "0":
    print()
    print("Работа программы завершена.")
    conn.close()
    raise SystemExit

if doc_filter == "4":
    print()
    print("=" * 70)
    print("СПРАВКА")
    print("=" * 70)
    print()
    print("MR - Руководства по ремонту.")
    print("     Содержат инструкции по разборке, сборке,")
    print("     регулировкам, моментам затяжки и ремонту.")
    print()
    print("NT - Технические ноты Renault.")
    print("     Содержат сервисные бюллетени,")
    print("     рекомендации завода и описание")
    print("     специальных технологий ремонта.")
    print()
    input("Нажмите Enter для продолжения...")
#    continue

while True:

    text = input("\nЧто искать (Enter — выход): ").strip()

    if text == "":
        break

# ==========================================================
# Выбор SQL-запроса по типу документа
# ==========================================================

if doc_filter == "1":

    sql = """
    SELECT
        doc_type,
        numero,
        titre,
        element_name
    FROM documents
    WHERE
        doc_type='NT'
        AND
        (
            titre LIKE ?
            OR element_name LIKE ?
        )
    ORDER BY numero
    LIMIT 10000
    """

    cur.execute(sql, ("%" + text + "%", "%" + text + "%"))


elif doc_filter == "2":

    sql = """
    SELECT
        doc_type,
        numero,
        titre,
        element_name
    FROM documents
    WHERE
        doc_type='MR'
        AND
        (
            titre LIKE ?
            OR element_name LIKE ?
        )
    ORDER BY numero
    LIMIT 10000
    """

    cur.execute(sql, ("%" + text + "%", "%" + text + "%"))


else:

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
    LIMIT 10000
    """

    cur.execute(sql, ("%" + text + "%", "%" + text + "%"))

rows = cur.fetchall()

print()

if len(rows) == 0:
        print("Ничего не найдено.")
        continue

print(f"Найдено документов: {len(rows)}")
print("-" * 70)

for i, row in enumerate(rows, start=1):

        print(f"{i:3}. [{row[0]}] {row[1]}")
        print("     ", row[2])
        print("     ", row[3])
        print()
# ============================================================
# НАЧАЛО ВСТАВКИ №3
# Выбор документа и открытие PDF
# ============================================================

    print()
    choice = input("Введите номер документа (Enter - новый поиск): ").strip()

    if choice == "":
        continue

    try:
        n = int(choice) - 1

        if n < 0 or n >= len(rows):
            print("Неверный номер.")
            continue

        row = rows[n]

        doc_type = row[0]
        numero = row[1]

        if doc_type not in PDF_FOLDERS:
            print("Неизвестный тип документа:", doc_type)
            continue

        pdf = os.path.join(PDF_FOLDERS[doc_type], numero + ".pdf")

        print()
        print("Открываю:")
        print(pdf)

        if os.path.exists(pdf):
            os.startfile(pdf)
        else:
            print("Файл не найден.")

    except ValueError:
        print("Нужно ввести номер.")

# ============================================================
# КОНЕЦ ВСТАВКИ №3
# ============================================================
conn.close()

        
