"""Phase gate demo: start at |+>, apply T eight times for a full Z-rotation."""

import matplotlib.pyplot as plt

from blochviz import H, T, animate_circuit

# T^8 = I, so 8 T gates complete one full revolution around Z
gates = [T] * 8
labels = [f"T^{i + 1}" for i in range(8)]

anim = animate_circuit(
    initial_state=[1, 0],
    gates=[H] + gates,
    labels=[r"$H \rightarrow |+\rangle$"] + labels,
    n_frames=35,
    interval=45,
    trail=True,
)

plt.tight_layout()
plt.show()
