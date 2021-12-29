import os
import csv
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np


root_dir = r'data/丫角视频'
file_name = 'NSY_STAGE_R_202112281555_if.csv'
output_file_name = file_name.replace('.csv', '_mf.csv')
file_path = os.path.join(root_dir, file_name)
output_file_path = os.path.join(root_dir, output_file_name)

step = 12
column = 3
skip = 241
p = 2

with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    head = next(reader)

    rows = list(reader)
    n_rows = rows.copy()
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

                if x.shape[0] <= 5:
                    regressor = LinearRegression()
                    regressor.fit(x, y)

                    predict_value = regressor.predict(predict_x)[0][0]
                    n_rows[index][column] = predict_value
                else:
                    poly = PolynomialFeatures(degree=p)
                    x_poly = poly.fit_transform(x)
                    regressor_poly = LinearRegression()
                    regressor_poly.fit(x_poly, y)

                    predict_value = regressor_poly.predict(poly.transform(predict_x))[0][0]
                    n_rows[index][column] = predict_value

                fix_count += 1


