import plotly.graph_objects as go
import pandas as pd
import sympy as sym
sym.init_printing()
from matrix import *

a1, a2, a3, a4 = 0.08, 0.39, 0, 0.32
def FK(q1,q2,q3,q4,q5):

    T01 = np.eye(4)
    T12 = Rx(q1) @ Tx(a1)  # Joint 1 to 2
    T23 = Ry(q2) @ Tz(a2)  # np.eye(4)# Joint 2 to 3
    T34 = Rz(q3) @ Rx(q4) @ Tz(a3+a4)  # Joint 3 to 4
    T45 = np.eye(4)#Tz(a3)  # Rx(q3)                    # Joint 4 to 5
    T56 = np.eye(4)#Tz(a4)  # Rz(q5) @ Tz(a3)           # Joint 5 to 6
    T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56

    x_pos = T06[0, -1]
    y_pos = T06[1, -1]
    z_pos = T06[2, -1]
    return x_pos, y_pos, z_pos

data= pd.read_csv("q_pointcloud_reduced.csv")

q1 = data['q1'].values.tolist()
q2 = data['q2'].values.tolist()
q3 = data['q3'].values.tolist()
q4 = data['q4'].values.tolist()
q5 = data['q5'].values.tolist()
X = []
Y = []
Z = []
for i in range(len(q5)):
    # x, y, z = FK(q1[i],q2[i],q3[i],q4[i],q5[i])
    x, y, z = FK(q1[i],q2[i],q3[i],q4[i],q5[i])
    X.append(x)
    Y.append(y)
    Z.append(z)

fig2 = go.Figure(data=[go.Scatter3d(x=X, y=Y, z=Z, mode='markers', marker=dict(
        size=2,
        color=z,                # set color to an array/list of desired values
        colorscale='Viridis',   # choose a colorscale
        opacity=0.8
    ))])

T01 = np.eye(4)
T12 = Rx(0) @ Tx(a1)  # Joint 1 to 2
T23 = Ry(0) @ Tz(a2)  # np.eye(4)# Joint 2 to 3
T34 = Rz(0) @ Rx(0)  # Joint 3 to 4
T45 = Tz(a3)  # Rx(q3)                    # Joint 4 to 5
T56 = Tz(a4)  # Rz(q5) @ Tz(a3)           # Joint 5 to 6
T67 = np.eye(4)  # Rx(q6)                    # Joint 6 to 7
T7E = np.eye(4)  # Rz(q7) @ Tz(a4)           # Joint 7 to E

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
fig2.add_trace(go.Scatter3d(x=x_pos, y=y_pos, z=z_pos,
                                   mode='lines+markers',marker_color='rgba(152, 13, 0, .8)',marker=dict(
            color='LightSkyBlue',
            size=8,
            line=dict(
                color="aliceblue",
                width=8
            )
        )))
fig2.update_yaxes(range=[-1, 1])
fig2.update_xaxes(range=[-1, 1])
fig2.show()
