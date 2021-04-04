import csv
import re


class PhonebookNormaliser:
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

    def __init__(self, file_path):
        self.file_path = file_path
        self.converted_rows = []
        self.fixed_info_list = []

    def get_data(self):
        with open(self.file_path, encoding='utf-8') as f:
            rows = csv.reader(f, delimiter=",")
            return list(rows)

    def text_normalizer(self, text_list):
        for word in text_list:
            if not word:
                continue
            for split_words in word.split():
                yield split_words

    def row_converter(self, text):
        text = ','.join(text)
        for key, item in self.pattern_dict.items():
            text = re.sub(item['in'], item['out'], text)
        return text.split(',')

    def list_converter(self, row):
        if len((row[0]).split()) == 2:
            row.insert(3, '')
        row = self.row_converter(row)
        row[:3] = self.text_normalizer(row[:3])
        return row

    def join_data(self, data_list):
        for i in range(len(data_list)):
            for j in range(len(data_list)):
                if data_list[i][0] == data_list[j][0]:
                    data_list[i] = [x or y for x, y in zip(data_list[i], data_list[j])]
            if data_list[i] not in self.fixed_info_list:
                self.fixed_info_list.append(data_list[i])
        return self.fixed_info_list

    def csv_writer(self, contacts_list):
        with open("phonebook.csv", "w") as file:
            datawriter = csv.writer(file, delimiter=',')
            datawriter.writerows(contacts_list)

    def main(self):
        contact_list = self.get_data()
        for row in contact_list:
            self.converted_rows.append(self.list_converter(row))
        res = self.join_data(self.converted_rows)
        self.csv_writer(res)


if __name__ == '__main__':
    PhonebookNormaliser("phonebook_raw.csv").main()
