import time
import numpy as np
import sympy as sym
from matrix import *
sym.init_printing()
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from math import atan2, sqrt
import matplotlib.pyplot as plt
from IPython.display import clear_output
import pandas
a1, a2, a3, a4 = 0.36, 0.42, 0.4, 0.126
pi = np.pi
pi_sym = sym.pi


def weighted_pseudo(q0, p_goal, weights=[10, 30, 25, 20, 90, 42, 57], time_step=0.1, max_iteration=3000,
                    accuracy=0.001):
    assert np.linalg.norm(p_goal) < 0.85 * np.sum([a1, a2, a3, a4]), "Robot Length constraint violated"

    q_n0 = q0
    p = FK(q_n0)[:3, -1]
    t1_dot = p_goal - p
    e = np.linalg.norm(t1_dot)

    Tt = np.eye(6)[:3]
    v1 = np.zeros(3)
    q_n1 = q_n0
    q_dot = np.zeros(len(q0))
    δt = time_step
    i = 0

    start_time = time.time()
    while True:
        if (e < accuracy):
            break

        fk = FK(q_n0)

        p = fk[:3, -1]

        t1_dot = p_goal - p

        e = np.linalg.norm(t1_dot)

        J1 = jacobian(q_n0)[:3]

        w_inv = np.linalg.inv(np.diag(weights))
        j1_hash = w_inv @ J1.T @ np.linalg.inv(J1 @ w_inv @ J1.T)

        q_dot = j1_hash @ t1_dot

        q_n1 = q_n0 + (δt * q_dot)

        q_n0 = q_n1

        i += 1
        if (i > max_iteration):
            print("No convergence")
            break

    end_time = time.time()
    print(f"to {np.round(p_goal, 2)} :: {np.round(end_time - start_time, 4)} seconds\n")

    return np.mod(q_n1, 2 * np.pi)


def jacobian_sym():
  q1, q2, q3, q4, q5, q6, q7 = sym.symbols("q_1 q_2 q_3 q_4 q_5 q_6 q_7", real=True)

  variables = [q1, q2, q3, q4, q5, q6, q7]

  TF =  Rz_sym(q1) @ Tz_sym(a1) @ \
        Rx_sym(q2)              @ \
        Rz_sym(q3) @ Tz_sym(a2) @ \
        Rx_sym(q4)              @ \
        Rz_sym(q5) @ Tz_sym(a3) @ \
        Rx_sym(q6)              @ \
        Rz_sym(q7) @ Tz_sym(a4)

  R = TF[:3,:-1]
  jacobian = sym.Matrix([])

  for var in variables:
      T_d  = sym.diff(TF, var)

      T    = T_d[0:3, -1]
      R_d  = T_d[0:3, :-1]
      R_j  = R_d @ R.T

      J = T.row_insert(3, sym.Matrix([R_j[2,1], R_j[0,2], R_j[1,0]]))

      jacobian = jacobian.col_insert(len(jacobian), J)

  return sym.lambdify([variables], jacobian, "numpy")

jacobian_sym_func = jacobian_sym()

def jacobian(joint_params):
    variables = [*joint_params]
    return jacobian_sym_func(variables)

def euler_angles(R, sndSol=True):
  rx = atan2(R[2,0], R[2,1])
  ry = atan2(sqrt(R[0,2]**2 + R[1,2]**2), R[2,2])
  rz = atan2(R[0,2], -R[1,2])

  return [rx, ry, rz]

def FK(joint_params):
  """
  Joint variables consisting of 7 parameters
  """
  joint_params = np.asarray(joint_params, dtype=float)
  q1, q2, q3, q4, q5, q6, q7 = joint_params
  TF = np.linalg.multi_dot([
          Rz(q1), Tz(a1),           # Joint 1 to 2
          Rx(q2),                   # Joint 2 to 3
          Rz(q3), Tz(a2),           # Joint 3 to 4
          Rx(q4),                   # Joint 4 to 5
          Rz(q5), Tz(a3),           # Joint 5 to 6
          Rx(q6),                   # Joint 6 to 7
          Rz(q7), Tz(a4)            # Joint 7 to E
  ])
  return TF

def plot_robots(rob_cnfs, traj_x, traj_y, traj_z, traj_fun=(lambda x, y: 0.5 + 0.5 * np.sin(3 * x * y))):
    """
    rob_cnfs: list of robot configurations and plots each conf
    traj_fun: function defined in terms of x and y and plots the 3D function
    representing the desired trajectory
    """
    fig = go.Figure()
    fig.add_scatter3d(
        x=traj_x,
        y=traj_y,
        z=traj_z,
        hoverinfo='none',
        marker=dict(size=0.1),
        name="desired trajectory"
    )

    for i, q_params in enumerate(rob_cnfs):
        q1, q2, q3, q4, q5, q6, q7 = q_params

        T01 = np.eye(4)
        T12 = Rz(q1) @ Tz(a1)  # Joint 1 to 2
        T23 = Rx(q2)  # Joint 2 to 3
        T34 = Rz(q3) @ Tz(a2)  # Joint 3 to 4
        T45 = Rx(q4)  # Joint 4 to 5
        T56 = Rz(q5) @ Tz(a3)  # Joint 5 to 6
        T67 = Rx(q6)  # Joint 6 to 7
        T7E = Rz(q7) @ Tz(a4)  # Joint 7 to E

        T02 = T01 @ T12
        T03 = T01 @ T12 @ T23
        T04 = T01 @ T12 @ T23 @ T34
        T05 = T01 @ T12 @ T23 @ T34 @ T45
        T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56
        T07 = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T67
        T0E = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T67 @ T7E

        x_pos = [T01[0, -1], T02[0, -1], T03[0, -1], T04[0, -1], T05[0, -1], T06[0, -1], T07[0, -1], T0E[0, -1]]
        y_pos = [T01[1, -1], T02[1, -1], T03[1, -1], T04[1, -1], T05[1, -1], T06[1, -1], T07[1, -1], T0E[1, -1]]
        z_pos = [T01[2, -1], T02[2, -1], T03[2, -1], T04[2, -1], T05[2, -1], T06[2, -1], T07[2, -1], T0E[2, -1]]

        # Setting opacity
        if (i != 0 and i != len(rob_cnfs) - 1):
            opc = 0.3
        else:
            opc = 1

        # Width
        wd = 10

        fig.add_scatter3d(
            x=np.round(x_pos, 2),
            y=np.round(y_pos, 2),
            z=z_pos,
            line=dict(color='darkblue', width=wd),
            hoverinfo="text",
            hovertext=[f"joint {idx}: {q}"
                       for idx, q in
                       enumerate(np.round(np.rad2deg([0, q1, q2, q3, q4, q5, q6, q7]), 0))],
            marker=dict(
                size=wd / 2,
                color=["black", "orange", "yellow", "pink", "blue", "goldenrod", "green", "red"],
                # colorscale='Viridis',
            ),
            opacity=opc,
            showlegend=False,
            name=f"conf {i}"
        )

    fig.layout = dict(
        width=1000,
        height=700,
        scene=dict(
            camera=dict(eye={'x': -1.25, 'y': -1.25, 'z': 2}),
            aspectratio={'x': 1.25, 'y': 1.25, 'z': 1},
            xaxis=dict(nticks=8, range=[np.min(traj_x) - 0.5, np.max(traj_x) + 0.5]),
            yaxis=dict(nticks=8, range=[np.min(traj_y) - 0.5, np.max(traj_y) + 0.5]),
            zaxis=dict(nticks=8, range=[-0.05, np.max(traj_z) + 0.4]),
            xaxis_title='Robot x-axis',
            yaxis_title='Robot y-axis',
            zaxis_title='Robot z-axis'),
        title=f"Robot plot in different configurations",
        colorscale=dict(diverging="thermal")
    )
    pio.show(fig)


# plot_robots([np.deg2rad([0,90,0,-90,0,90,0]), np.deg2rad([0,0,0,0,0,0,0]), np.deg2rad([0,-90,0,90,0,-90,0])])
def get_cnfs(method_fun, q0=np.deg2rad([0, 30, 0, -20, 0, 45, 0]), kwargs=dict()):
    """Returns all the joint configurations for the robot at different points on
      the required trajectory for a specific method"""

    x = np.hstack([
        [0.4 for _ in range(10)],
    ])

    y = np.hstack([
        np.linspace(-0.2, 0.4, 10),
    ])

    z = [0.9 for _ in x]

    # x = np.hstack([
    #         [ 0.4 for _ in range(5) ],
    #         [ 0.2 for _ in range(5)],
    #         np.linspace(0.2, 0.4, 5),
    #         np.linspace(0.2, 0.4, 5) ])

    # y = np.hstack([
    #         np.linspace(0.2, 0.4, 5),
    #         np.linspace(0.2, 0.4,5),
    #         [ 0.4 for _ in range(5) ],
    #         [ 0.2 for _ in range(5)]])

    # z = [ 0.9 for _ in x ]
    rob_cnfs = []  # will contain the result of each inverse kinematics

    start_time = time.time()

    for (i, j, k) in zip(x, y, z):
        pos = [i, j, k]

        q = method_fun(q0, pos, **kwargs)

        rob_cnfs.append(q)
        # q0 = q     # Sets the new initial joint configurations to the previous

    end_time = time.time()

    print(f"\n{np.round(end_time - start_time, 1)} seconds : Total time using {method_fun.__name__} \n")
    if kwargs: print(f"\nParameters used: {kwargs}")

    plot_robots(rob_cnfs, traj_x=x, traj_y=y, traj_z=z)


def null_space_method(q0, p_goal, weights=[1, 3, 1, 2, 9, 4, 5], time_step=0.01, max_iteration=3000, accuracy=0.01):
    assert np.linalg.norm(p_goal[:3]) <= 0.85 * np.sum([a1, a2, a3, a4]), "Robot Length constraint violated"

    q_n0 = q0
    p = FK(q_n0)[:3, -1]
    t_dot = p_goal[:3] - p
    H1 = [0, 0, 0, 0, 0, 0, 0]
    e = np.linalg.norm(t_dot)

    Tt = np.block([np.eye(3), np.zeros((3, 3))])
    q_n1 = q_n0
    δt = time_step
    q_dot_0 = [4, 9, 1, 7, 9, 5, 1]  # [ 0.4, 0.9, 0.1, 0.7, 0.9, 0.5, 0.22]
    i = 0

    start_time = time.time()
    while True:
        if (e < accuracy):
            break

        fk = FK(q_n0)

        rx, ry, rz = euler_angles(fk[:3, :3])

        p = np.hstack([fk[:3, -1], [rx, ry, rz]])  # current position and orientation

        t_dot = p_goal[:3] - p[:3]

        e = np.linalg.norm(t_dot)

        w_inv = np.linalg.inv(np.diag(weights))

        Jt = np.dot(Tt, jacobian(q_n0))

        j_hash = w_inv @ Jt.T @ np.linalg.inv(Jt @ w_inv @ Jt.T)

        q_dot = (j_hash @ t_dot) + (np.eye(7) - (j_hash @ Jt)) @ q_dot_0

        q_n1 = q_n0 + (δt * q_dot)

        # H2 = np.sqrt(np.linalg.det(Jt@Jt.T))

        # dH = H2 - H1

        # dq = q_n1 - q_n0

        # grad_Hq = np.divide(dH, dq)

        # H2 = []
        # for i,q in enumerate(q_n1):
        #   q_i = q_n1          # np.zeros(7)
        #   q_i[i]=q-q_n0[i]
        #   Jt_i = np.dot(Tt, jacobian(q_i))

        #   H2.append(np.sqrt(np.linalg.det(Jt_i@Jt_i.T)))

        # grad_Hq = np.asarray(H2) - np.asarray(H1)

        # q_dot_0 = grad_Hq.T

        q_n0 = q_n1
        # H1 = H2

        i += 1
        if (i > max_iteration):
            print("No convergence")
            break

    end_time = time.time()
    print(f"to {np.round(p_goal, 2)} :: time taken {np.round(end_time - start_time, 4)} seconds\n")

    return np.mod(q_n1, 2 * np.pi)


get_cnfs(method_fun=weighted_pseudo, q0=np.deg2rad([10,-10,0,20,0,-60,0]))