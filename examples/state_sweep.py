"""State sweep: Ry(theta) from 0 to pi, tracing the |0>->|1> meridian arc."""

import matplotlib.pyplot as plt
import numpy as np

from blochviz import Ry, animate_circuit

N = 20
step = np.pi / N
gates = [Ry(step)] * N
labels = [rf"$R_y({i + 1}\pi/{N})$" for i in range(N)]

anim = animate_circuit(
    initial_state=[1, 0],
    gates=gates,
    labels=labels,
    n_frames=20,
    interval=60,
    trail=True,
)

plt.tight_layout()
plt.show()
