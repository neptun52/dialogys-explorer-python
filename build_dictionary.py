import os
import json

# ------------------------------------------------------------
# Настройки
# ------------------------------------------------------------

DICT_PATH = r"D:\DialogysExplorer\dictionary"

ELEMENTS_FILE = os.path.join(DICT_PATH, "elements.txt")
OPERATIONS_FILE = os.path.join(DICT_PATH, "operations.txt")
TITLES_FILE = os.path.join(DICT_PATH, "titles.txt")

OUTPUT_FILE = os.path.join(
    DICT_PATH,
    "dialogys_dictionary.json"
)

# ------------------------------------------------------------
# Чтение текстового файла
# ------------------------------------------------------------

def load_list(filename):

    data = []

    with open(filename, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if line != "":
                data.append(line)

    return sorted(set(data))

# ------------------------------------------------------------
# Создание словаря
# ------------------------------------------------------------

dictionary = {

    "elements": {},
    "operations": {},
    "titles": {}

}

# ------------------------------------------------------------
# Элементы
# ------------------------------------------------------------

for item in load_list(ELEMENTS_FILE):

    dictionary["elements"][item] = ""

# ------------------------------------------------------------
# Операции
# ------------------------------------------------------------

for item in load_list(OPERATIONS_FILE):

    dictionary["operations"][item] = ""

# ------------------------------------------------------------
# Документы
# ------------------------------------------------------------

for item in load_list(TITLES_FILE):

    dictionary["titles"][item] = ""

# ------------------------------------------------------------
# Сохранение JSON
# ------------------------------------------------------------

with open(
    OUTPUT_FILE,
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

print()
print("=" * 60)
print("Словарь успешно создан.")
print("=" * 60)

print()

print("Элементов :", len(dictionary["elements"]))
print("Операций  :", len(dictionary["operations"]))
print("Документов:", len(dictionary["titles"]))

print()

print("Файл сохранён:")
print(OUTPUT_FILE)

print("=" * 60)