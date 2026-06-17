"""State sweep: Ry(θ) from θ=0 to π, tracing the |0⟩→|1⟩ meridian arc."""

import matplotlib.pyplot as plt
import numpy as np

from blochviz import Ry, animate_circuit

N = 20
step = np.pi / N
gates = [Ry(step)] * N
labels = [f"Ry({i + 1}π/{N})" for i in range(N)]

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
