"""Superposition: H places the qubit on the equator; phase rotations sweep it."""

import matplotlib.pyplot as plt
import numpy as np

from blochviz import H, Rz, animate_circuit

# H creates superposition (north pole -> equator).
# Eight Rz(pi/4) steps complete one full phase cycle on the equator.
# A final H converts phase back to amplitude (equator -> |0>).
gates = [H] + [Rz(np.pi / 4)] * 8 + [H]
labels = (
    [r"$H$: create $|{+}\rangle$"]
    + [rf"$R_z(\pi/4) \times {i + 1}$  [phase rotation]" for i in range(8)]
    + [r"$H$: phase -> amplitude  ->  $|0\rangle$"]
)

anim = animate_circuit(
    initial_state=[1, 0],
    gates=gates,
    labels=labels,
    n_frames=40,
    interval=35,
    trail=True,
)

plt.suptitle("Superposition and phase", color="white", fontsize=13)
plt.tight_layout()
plt.show()
