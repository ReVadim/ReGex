import csv
import re


pattern_dict = {
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

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def text_normalizer(text_list):
    for word in text_list:
        if not word:
            continue
        for split_words in word.split():
            yield split_words


def row_converter(text):
    text = ','.join(text)
    for key, item in pattern_dict.items():
        text = re.sub(item['in'], item['out'], text)
    return text.split(',')


def list_converter(text_list):
    converted_rows = []
    for row in text_list:
        if len((row[0]).split()) == 2:
            row.insert(3, '')
        row = row_converter(row)
        row[:3] = text_normalizer(row[:3])
        converted_rows.append(row)
    return converted_rows


def join_data(data_list):
    fixed_info_list = []
    for i in range(len(data_list)):
        for j in range(len(data_list)):
            if data_list[i][0] == data_list[j][0]:
                data_list[i] = [x or y for x, y in zip(data_list[i], data_list[j])]
        if data_list[i] not in fixed_info_list:
            fixed_info_list.append(data_list[i])
    return fixed_info_list


result = join_data(list_converter(contacts_list))
# for line in result:
#     print(line)

with open("phonebook.csv", "w") as file:
    datawriter = csv.writer(file, delimiter=',')
    datawriter.writerows(result)
