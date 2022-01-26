import numpy as np

angle1 = 0
omega1 = 0
angle2 = 0
omega2 = 0

a1 = float(input())
a2 = a1
for i in range(100):
    angle1 += omega1
    omega1 -= 0.1 * np.sin(a1)
    a1 -= omega1

    angle2 += omega2
    omega2 -= a2 - a2 ** 3 / 3
    a2 -= omega2

print(round(abs(a2 - a1), 2))