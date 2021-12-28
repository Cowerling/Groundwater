import os
import csv
import datetime


root_dir = r'C:\Users\Cowerling\Desktop\__利辛视频__'
file_name = 'ST_SOIL_R_202112281645.csv'
output_file_name = file_name.replace('.csv', '_if.csv')
file_path = os.path.join(root_dir, file_name)
output_file_path = os.path.join(root_dir, output_file_name)

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    head = next(reader)

    rows = list(reader)

    currentDatetime = datetime.datetime.strptime(rows[0][1], "%Y-%m-%d %H:%M:%S.%f")
    endDatetime = datetime.datetime.strptime(rows[-1][1], "%Y-%m-%d %H:%M:%S.%f")
    offset = datetime.timedelta(hours=1)

    full_data = {}

    while currentDatetime != endDatetime + offset:
        full_data[currentDatetime] = None

        currentDatetime = currentDatetime + offset

    for row in rows:
        full_data[datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f")] = row

    fail_count = 0

    with open(output_file_path, 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.writer(out_file)

        writer.writerow(head)

        for (time, value) in full_data.items():
            if value is None:
                value = ['' for _ in head]
                value[1] = time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                fail_count += 1

            writer.writerow(value)

    print('ok: {}%'.format(round((len(full_data) - fail_count) / len(full_data) * 100, 2)))
