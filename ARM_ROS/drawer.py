# import csv
# file = open("/home/r/PycharmProjects/ARM_ex/ARM_ROS/data_point.csv")
# csvreader = csv.reader(file)
# header = next(csvreader)
# print(header)
# rows = []
# for row in csvreader:
#     rows.append(row)
# print(rows)
# file.close()
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

headers = ['time', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']

df = pd.read_csv('/home/r/PycharmProjects/ARM_ex/ARM_ROS/data_point.csv', names=headers)

df.set_index('time').plot()

plt.show()