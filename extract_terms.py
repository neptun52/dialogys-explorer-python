import os
import xml.etree.ElementTree as ET

# -----------------------------------------------------
# Настройки
# -----------------------------------------------------

INDEX_PATH = r"D:\Program Files1\Dialogys\data\mrnt\fr\d3k\indexation"

OUT_DIR = "dictionary"

# -----------------------------------------------------

elements = set()
operations = set()
titles = set()

os.makedirs(OUT_DIR, exist_ok=True)

# -----------------------------------------------------

for file in os.listdir(INDEX_PATH):

    if not file.lower().endswith(".xml"):
        continue

    full_name = os.path.join(INDEX_PATH, file)

    print("Сканируется:", file)

    try:

        tree = ET.parse(full_name)
        root = tree.getroot()

    except Exception as e:

        print("Ошибка:", file)
        print(e)
        continue

    # ---------------------------------------
    # элементы
    # ---------------------------------------

    for element in root.iter("element"):

        name = element.get("lib")

        if name:
            elements.add(name.strip())

    # ---------------------------------------
    # операции
    # ---------------------------------------

    for operation in root.iter("operation"):

        name = operation.get("libelle")

        if name:
            operations.add(name.strip())

    # ---------------------------------------
    # документы
    # ---------------------------------------

    for pdf in root.iter("pdf"):

        title = pdf.get("titre")

        if title:
            titles.add(title.strip())

# -----------------------------------------------------
# Сохранение
# -----------------------------------------------------

def save(filename, data):

    with open(
        os.path.join(OUT_DIR, filename),
        "w",
        encoding="utf-8"
    ) as f:

        for item in sorted(data):

            f.write(item + "\n")

save("elements.txt", elements)
save("operations.txt", operations)
save("titles.txt", titles)

# -----------------------------------------------------

print()
print("=" * 60)

print("Готово.")

print("Элементов :", len(elements))
print("Операций  :", len(operations))
print("Документов:", len(titles))

print("=" * 60)