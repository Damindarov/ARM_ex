import csv
import pandas as pd
import matplotlib.pyplot as plt

print(pd.__version__)

kuka_time_iiwa2 = []
kuka_time_speed = []
kuka_time_listener = []
kuka_pos_q1 = []
kuka_speed = []
kuka_listener = []
time_delta = 1651615425811520487
with open('/home/r/PycharmProjects/ARM_ex/ARM_ROS/my/datas_iiwa2.txt') as f:
    for line in f:
        l = line.split(", ")
        t = l[0][4:]
        t = (float(t) - time_delta)/1000000000
        kuka_time_iiwa2.append(t)

        q1 = l[1]
        q1 = float(q1)
        print(t, q1)
        kuka_pos_q1.append(q1)
with open('/home/r/PycharmProjects/ARM_ex/ARM_ROS/my/datas_iiwa2_speed.txt') as f:
    for line in f:
        l = line.split(", ")
        t = l[0][4:]
        t = (float(t)-time_delta)/1000000000
        kuka_time_speed.append(t)

        q1 = l[1]
        q1 = float(q1)
        print(t, q1)
        kuka_speed.append(q1)
with open('/home/r/PycharmProjects/ARM_ex/ARM_ROS/my/datas_iiwa2_listener.txt') as f:
    for line in f:
        l = line.split(", ")
        t = l[0][4:]
        t = (float(t)-time_delta)/1000000000
        kuka_time_listener.append(t)

        q1 = l[1]
        q1 = float(q1)
        print(t, q1)
        kuka_listener.append(q1)
#
data = pd.read_csv("/home/r/PycharmProjects/ARM_ex/ARM_ROS/my/data_point_ROS_part.csv")
arm_time = data['time'].values
arm_time_m = [(i-time_delta)/1000000000 for i in arm_time]
# force.torque.a4/0.8 + 3.14/4 + 3.14/2
# time,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
arm_pos_q1 = data['q6'].values
print(arm_pos_q1)
# # data2 = pd.read_csv("/home/r/PycharmProjects/ARM_ex/points_exo_server.csv")
# # arm_time2 = data2['time'].values
# # arm_time_m2 = [i * 1000000000 for i in arm_time2]
# # arm_pos_q12 = data2['q1'].values

import plotly.graph_objects as go
import plotly.express as px


colors = px.colors.qualitative.Plotly
fig = go.Figure()
fig.add_traces(go.Scatter(x=kuka_time_iiwa2, y = kuka_pos_q1, mode = 'lines', line=dict(color=colors[0]), name ="Points ROS_C++3"))
fig.add_traces(go.Scatter(x=arm_time_m, y = arm_pos_q1, mode = 'lines', line=dict(color=colors[1]),name="raspberry1"))
fig.add_traces(go.Scatter(x=kuka_time_speed, y = kuka_speed, mode = 'lines', line=dict(color=colors[2]), name ="kuka_speed4"))
fig.add_traces(go.Scatter(x=kuka_time_listener, y = kuka_listener, mode = 'lines', line=dict(color=colors[3]), name ="kuka_listener2"))

# fig.add_traces(go.Scatter(x=df['id'], y = df['c'], mode = 'lines', line=dict(color=colors[2])))
fig.show()



# fig, ax = plt.subplots()
# ax.plot(kuka_time, kuka_pos_q1, label="Points ROS_C++")
# ax.plot(arm_time_m, arm_pos_q1, label="raspberry")
# # ax.plot(arm_time_m2, arm_pos_q12, label="ROS_part")
# ax.legend()
#
# plt.show()