import csv
import pandas as pd
import matplotlib.pyplot as plt

print(pd.__version__)

kuka_time = []
kuka_pos_q1 = []
with open('/home/r/catkin_ws/New_points_Kuka.txt') as f:
    for line in f:
        l = line.split(", ")
        t = l[0][4:]
        t = int(t)
        kuka_time.append(t)

        q1 = l[1]
        q1 = float(q1)
        kuka_pos_q1.append(q1)

data = pd.read_csv("/home/r/PycharmProjects/ARM_ex/ARM_ROS/data_point.csv1")
arm_time = data['time'].values
arm_time_m = [i * 1000000000 for i in arm_time]
arm_pos_q1 = data['q1'].values

fig, ax = plt.subplots()
ax.plot(kuka_time, kuka_pos_q1, label="Kuka")
ax.plot(arm_time_m, arm_pos_q1, label="arm")
ax.legend()

plt.show()