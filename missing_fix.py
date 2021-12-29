import os
import csv
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import copy

root_dir = r'data/利辛视频'
file_name = 'ST_SOIL_R_40_202112281645_if.csv'
output_file_name = file_name.replace('.csv', '_mf.csv')
file_path = os.path.join(root_dir, file_name)
output_file_path = os.path.join(root_dir, output_file_name)

step = 12
skip = 0
p = 2
column = 3
max_value = 100

if 'ST_SOIL_R_10' in file_name:
    column = 5
elif 'ST_SOIL_R_20' in file_name:
    column = 6
elif 'ST_SOIL_R_40' in file_name:
    column = 8

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    head = next(reader)

    rows = list(reader)
    n_rows = copy.deepcopy(rows)
    fix_count = 0

    for index, row in enumerate(rows):
        if index < skip:
            continue

        if row[column] == '' or float(row[column]) == 0:
            pre_index = index - step
            if pre_index < 0:
                pre_index = 0

            next_index = index + step
            if next_index >= len(rows):
                next_index = len(rows) - 1

            sub_rows = rows[pre_index: next_index + 1]
            x = []
            y = []

            for sub_index, sub_row in enumerate(sub_rows):
                if sub_row[column] != '' and float(sub_row[column]) != 0:
                    x.append(sub_index)
                    y.append(sub_row[column])

            if len(x) > 1:
                x = np.expand_dims(np.array(x), axis=1)
                y = np.expand_dims(np.array(y), axis=1)
                predict_x = [[index - pre_index]]

                if x.shape[0] <= step:
                    regressor = LinearRegression()
                    regressor.fit(x, y)

                    predict_value = regressor.predict(predict_x)[0][0]
                    n_rows[index][column] = round(predict_value, 3)
                else:
                    poly = PolynomialFeatures(degree=p)
                    x_poly = poly.fit_transform(x)
                    regressor_poly = LinearRegression()
                    regressor_poly.fit(x_poly, y)

                    predict_value = regressor_poly.predict(poly.transform(predict_x))[0][0]
                    n_rows[index][column] = round(predict_value, 3)

                fix_count += 1

    for n_index, n_row in enumerate(n_rows):
        if n_row[column] == '' or float(n_row[column]) == 0:
            pre_n_index = n_index - 1
            while pre_n_index >= 0 and (n_rows[pre_n_index][column] == '' or float(n_rows[pre_n_index][column]) == 0):
                pre_n_index -= 1

            next_n_index = n_index + 1
            while next_n_index < len(n_rows) and (n_rows[next_n_index][column] == '' or float(n_rows[next_n_index][column]) == 0):
                next_n_index += 1

            if pre_n_index >= 0 and n_index - pre_n_index <= step * 2 and next_n_index < len(n_rows) and next_n_index - n_index <= step * 2:
                n_x = np.expand_dims(np.array([0, next_n_index - pre_n_index]), axis=1)
                n_y = np.expand_dims(np.array([n_rows[pre_n_index][column], n_rows[next_n_index][column]]), axis=1)

                n_regressor = LinearRegression()
                n_regressor.fit(n_x, n_y)

                for sub_n_index in range(pre_n_index + 1, next_n_index):
                    n_redict_x = [[sub_n_index - pre_n_index]]

                    n_predict_value = n_regressor.predict(n_redict_x)[0][0]
                    n_rows[sub_n_index][column] = n_predict_value

                    fix_count += 1

    with open(output_file_path, 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.writer(out_file)

        writer.writerow(head)

        for n_row in n_rows:
            if n_row[column] != '' and float(n_row[column]) == 0:
                n_row[column] = ''

            if n_row[column] != '' and float(n_row[column]) > max_value:
                n_row[column] = max_value

            writer.writerow(n_row)

    print(fix_count)
