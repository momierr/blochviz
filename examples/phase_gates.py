"""Gate effects: X, Z, H, Ry, Rz shown step by step from |0>."""

import matplotlib.pyplot as plt
import numpy as np

from blochviz import H, Ry, Rz, X, animate_circuit

# Circuit designed so each gate starts from a meaningful state
# and the trajectory returns to |0> at the end.
gates = [
    H,  # |0>  -> |+>   superposition
    X,  # |+>  -> |+>   (eigenstate: stays!)
    Z,  # |+>  -> |->   phase flip on equator
    H,  # |->  -> |1>   phase -> amplitude
    X,  # |1>  -> |0>   NOT gate: back to start
    Ry(np.pi / 2),  # |0>  -> |+>   smooth Y-rotation
    Rz(np.pi),  # |+>  -> |->   half-turn around Z
    Ry(-np.pi / 2),  # |->  -> |1>   Y-rotation down
    X,  # |1>  -> |0>   NOT gate: back to |0>
]
labels = [
    r"$H$: $|0\rangle \to |{+}\rangle$  (superposition)",
    r"$X$: eigenstate of $|{+}\rangle$ -- no change",
    r"$Z$: $|{+}\rangle \to |{-}\rangle$  (phase flip)",
    r"$H$: $|{-}\rangle \to |1\rangle$  (phase -> amplitude)",
    r"$X$: NOT gate  $|1\rangle \to |0\rangle$",
    r"$R_y(\pi/2)$: smooth rotation to $|{+}\rangle$",
    r"$R_z(\pi)$: half-turn around Z  $\to |{-}\rangle$",
    r"$R_y(-\pi/2)$: rotate down to $|1\rangle$",
    r"$X$: NOT gate back to $|0\rangle$",
]

anim = animate_circuit(
    initial_state=[1, 0],
    gates=gates,
    labels=labels,
    n_frames=45,
    interval=40,
    trail=True,
)

plt.suptitle(
    "Standard gate effects on the Bloch sphere", color="white", fontsize=13
)
plt.tight_layout()
plt.show()
