import numpy as np
from Test_Jacobian import*
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
        q_n0 = q_n1
        i += 1
        if (i > max_iteration):
            print("No convergence")
            break

    end_time = time.time()
    print(f"to {np.round(p_goal, 2)} :: time taken {np.round(end_time - start_time, 4)} seconds\n")

    return np.mod(q_n1, 2 * np.pi)