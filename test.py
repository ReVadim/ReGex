import csv
import re


pattern_dict = {
    'fio': {
        'in': r'([А-ЯЁ]\w+)\s*,*([А-ЯЁ]\w+)\s*,*([А-ЯЁ]\w+\s*)*',
        'out': r'\1 \2 \3'
    },
    'phone_num': {
        'in': r'(\+7\s*|8\s*)\(*(\d{3})\)*\s*-*(\d{3})-*\s*(\d{2})-*\s*(\d{2})',
        'out': r'8(\2)\3-\4-\5'
    },
    'dop_num': {
        'in': r'\(*([д][о][б])\s*(\.*)\s*(\d+)\)*',
        'out': r'доб.\3'
    },
    'e-mail': {
        'in': r'(\w+\.?\w+@([a-z0-9]+)\.([a-z]{2,4}))',
        'out': r'\1'
    }
}

new_dict = {}
output_list = []
# def csv_reader():
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for line in contacts_list:
    line = ','.join(line)
    for key, item in pattern_dict.items():
        line = re.sub(item['in'], item['out'], line)
    output_list.append(line)

# for row in output_list:
#     print(row)

with open("phonebook.csv", "w", encoding='utf-8') as phonebook:
    datawriter = csv.writer(phonebook, delimiter=',')
    datawriter.writerows(output_list)