"""Single-qubit gate sequence: H -> Rz(pi/4) -> H."""

import matplotlib.pyplot as plt
import numpy as np

from blochviz import H, Rz, animate_circuit

anim = animate_circuit(
    initial_state=[1, 0],
    gates=[H, Rz(np.pi / 4), H],
    labels=[r"$H$", r"$R_z(\pi/4)$", r"$H$"],
    n_frames=40,
    interval=40,
    trail=True,
)

plt.tight_layout()
plt.show()
