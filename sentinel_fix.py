import os
import json
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import csv


root_dir = r'data/丫角视频'
file_name = 'Sentinel-2_L2A.json'
output_file_name = file_name.replace('.json', '_sef.csv')
file_path = os.path.join(root_dir, file_name)
output_file_path = os.path.join(root_dir, output_file_name)

head = ['TIME', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B11', 'B12']

last_time = datetime.datetime.strptime('2021-12-31 00:00:00', '%Y-%m-%d %H:%M:%S')

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)['features']

    rows = []

    for sub_data in data:
        row = []

        sub_data = sub_data['properties']

        time = datetime.datetime.strptime(sub_data['index'].split('_')[1], '%Y%m%dT%H%M%S')
        time = datetime.datetime.strptime(time.strftime('%Y-%m-%d %H:00:00'), '%Y-%m-%d %H:%M:%S')

        row.append(time)

        if len(sub_data) != 1:
            for sub_head in head[1:]:
                row.append(sub_data[sub_head])

        rows.append(row)

    current_time = rows[0][0]
    end_time = rows[-1][0]

    offset = datetime.timedelta(hours=1)

    full_data = {}

    while current_time != end_time + offset:
        full_data[current_time] = ['' for _ in head]
        full_data[current_time][0] = current_time

        current_time = current_time + offset

    for row in rows:
        if len(row) > 1:
            full_data[row[0]] = row

    full_rows = list(full_data.values())

    for index, full_row in enumerate(full_rows):
        if full_row[1] == '':
            pre_index = index - 1
            while pre_index >= 0 and full_rows[pre_index][1] == '':
                pre_index -= 1

            next_index = index + 1
            while next_index < len(full_rows) and full_rows[next_index][1] == '':
                next_index += 1

            if pre_index >= 0 and next_index < len(full_rows):
                for column in range(1, len(head)):
                    x = np.expand_dims(np.array([0, next_index - pre_index]), axis=1)
                    y = np.expand_dims(np.array([full_rows[pre_index][column], full_rows[next_index][column]]), axis=1)

                    regressor = LinearRegression()
                    regressor.fit(x, y)

                    for sub_index in range(pre_index + 1, next_index):
                        predict_x = [[sub_index - pre_index]]

                        predict_value = regressor.predict(predict_x)[0][0]
                        full_rows[sub_index][column] = predict_value

    current_time = full_rows[-1][0]
    count = 1
    while current_time < last_time:
        full_row = ['' for _ in head]
        full_row[0] = current_time

        for column in range(1, len(head)):
            x = np.expand_dims(np.array([0, next_index - pre_index]), axis=1)
            y = np.expand_dims(np.array([full_rows[pre_index][column], full_rows[next_index][column]]), axis=1)

            regressor = LinearRegression()
            regressor.fit(x, y)

            predict_x = [[next_index - pre_index + count]]
            predict_value = regressor.predict(predict_x)[0][0]

            full_row[column] = predict_value

        full_rows.append(full_row)

        current_time = current_time + offset
        count += 1

    with open(output_file_path, 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.writer(out_file)

        writer.writerow(head)

        for full_row in full_rows:
            writer.writerow(full_row)

    print('ok')
