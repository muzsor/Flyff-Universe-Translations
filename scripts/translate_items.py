# Usage: pip install googletrans==4.0.0-rc1
#        python translate_items.py "c:\Users\mhermano\Desktop\repos\Flyff-Universe-Translations\Filipino\Items.csv"
import sys, csv, shutil, time
from googletrans import Translator

def translate_file(path):
    backup = path + ".bak"
    shutil.copy2(path, backup)
    translator = Translator()
    rows = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    # Header remains same
    for i in range(1, len(rows)):
        row = rows[i]
        # ensure at least 3 columns
        while len(row) < 3:
            row.append('')
        english = row[1].strip()
        if english == '':
            row[2] = ''
            continue
        # translate to Filipino (Tagalog) -> 'tl'
        try:
            tr = translator.translate(english, dest='tl')
            row[2] = tr.text
        except Exception as e:
            # on failure, keep original English in Filipino column to avoid data loss
            row[2] = english
        rows[i] = row
        time.sleep(0.05)  # gentle throttle

    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"Translated file saved. Backup written to: {backup}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide path to Items.csv")
        sys.exit(1)
    translate_file(sys.argv[1])
