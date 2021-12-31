import os
import csv


root_dir = r'data/丫角视频'
file_name = 'ALL.csv'
output_file_name = file_name.replace('.csv', '_sf.csv')
file_path = os.path.join(root_dir, file_name)
output_file_path = os.path.join(root_dir, output_file_name)

g_column = 1
p_column = 2
s_10_column = 3
s_20_column = 4
s_40_column = 5

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    head = next(reader)

    rows = list(reader)
    remove_count = 0
    fix_count = 0
    valid_sections = []

    for row in rows:
        if row[g_column] == '' or row[s_10_column] == '' or row[s_20_column] == '' or row[s_40_column] == '':
            for column in range(1, len(head)):
                row[column] = ''

            remove_count += 1
        else:
            if row[p_column] == '':
                row[p_column] = 0
                fix_count += 1

    with open(output_file_path, 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.writer(out_file)

        writer.writerow(head)

        pre_index = -1
        next_index = -1

        for index, row in enumerate(rows):
            if row[g_column] != '' and index != 0 and rows[index - 1][g_column] == '':
                pre_index = index

            if row[g_column] == '' and index != 0 and rows[index - 1][g_column] != '' and pre_index != -1:
                next_index = index - 1

            if pre_index != -1 and next_index != -1:
                valid_sections.append((pre_index, next_index, next_index - pre_index + 1))

                pre_index = -1
                next_index = -1

            writer.writerow(row)

    print(remove_count, fix_count)
    print(valid_sections)
