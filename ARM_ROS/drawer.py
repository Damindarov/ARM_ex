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
import plotly.express as px

df = pd.read_csv('/home/r/PycharmProjects/ARM_ex/ARM_ROS/data_point.csv')
df1 = pd.read_csv('/home/r/catkin_ws/points_Kuka.csv')

print(df)
print(df1.head())
fig = px.line(df, x = 'time', y = 'q1', title='Apple Share Prices over time (2014)')
fig1 = px.line(df1, x = 'time', y = 'q1', title='78епнг Share Prices over time (2014)')

fig.show()