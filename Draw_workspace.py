import plotly.graph_objects as go
import numpy as np
import pandas as pd
from matrix import *
import math
data = pd.read_csv("/content/point_cloud1.csv")
a1, a2, a3, a4 = 0.08, 0, 0.39, 0.32

q1, q2, q3, q4, q5 = [], [], [], [], []

x_pos, y_pos, z_pos = [], [], []
for i in range(len(data.values)):
  q1.append(float(data.values[i, 0]))
  q2.append(float(data.values[i, 1]))
  q3.append(float(data.values[i, 2]))
  q4.append(float(data.values[i, 3]))
  q5.append(float(data.values[i, 4]))



for i in range(len(q1)):
  T01 = np.eye(4) @ Ry(math.pi)
  T12 = Rx(q1[i]) @ Tx(a1)  # Joint 1 to 2
  T23 = Ry(q2[i])  # @ Tz(a2)  # Joint 2 to 3
  T34 = Rz(q3[i]) @ Tz(-a3)  # Joint 3 to 4
  T45 = Rx(q4[i]) @ Tz(-a4)  # Joint 4 to 5

  T56 = Rz(q5[i])  # @ Tz(a4)  # Joint 5 to 6

  T02 = T01 @ T12
  T03 = T01 @ T12 @ T23
  T04 = T01 @ T12 @ T23 @ T34
  T05 = T01 @ T12 @ T23 @ T34 @ T45
  T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56
  # T07 = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T67
  # T0E = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T67 @ T7E

  x_pos.append(T06[0][3])
  y_pos.append(T06[1][3])
  z_pos.append(T06[2][3])

fig = go.Figure()
fig.add_trace(go.Scatter3d(x=x_pos, y=y_pos, z=z_pos,
                                   mode='markers',marker=dict(
            color='LightSkyBlue',
            size=3,
            line=dict(
                color='MediumPurple',
                width=12
            )
        )))

T01 = np.eye(4)
T12 = Rx(0) @ Tx(-a1)           # Joint 1 to 2
T23 = Tz(-a2) #np.eye(4)# Joint 2 to 3
T34 = Rz(0)@Rx(0)           # Joint 3 to 4
T45 = Tz(-a3) #Rx(q3)                    # Joint 4 to 5
T56 = Tz(-a4)#Rz(q5) @ Tz(a3)           # Joint 5 to 6
T67 = np.eye(4)#Rx(q6)                    # Joint 6 to 7
T7E = np.eye(4)#Rz(q7) @ Tz(a4)           # Joint 7 to E

T02 = T01 @ T12
T03 = T01 @ T12 @ T23
T04 = T01 @ T12 @ T23 @ T34
T05 = T01 @ T12 @ T23 @ T34 @ T45
T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56
T07 = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T67
T0E = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T67 @ T7E
x_pos = [T01[0,-1], T02[0,-1], T03[0,-1], T04[0,-1], T05[0,-1], T06[0,-1], T07[0,-1], T0E[0,-1]]
y_pos = [T01[1,-1], T02[1,-1], T03[1,-1], T04[1,-1], T05[1,-1], T06[1,-1], T07[1,-1], T0E[1,-1]]
z_pos = [T01[2,-1], T02[2,-1], T03[2,-1], T04[2,-1], T05[2,-1], T06[2,-1], T07[2,-1], T0E[2,-1]]
fig.add_trace(go.Scatter3d(x=x_pos, y=y_pos, z=z_pos,
                                   mode='lines+markers',marker_color='rgba(152, 13, 0, .8)',marker=dict(
            color='LightSkyBlue',
            size=8,
            line=dict(
                color="aliceblue",
                width=8
            )
        )))
fig.update_yaxes(range=[-1, 1])
fig.update_xaxes(range=[-1, 1])
fig.show()