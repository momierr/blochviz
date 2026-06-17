"""Bell state |Phi+> preparation: |00> -> (H(x)I) -> CNOT -> |Phi+>."""

import matplotlib.pyplot as plt

from blochviz import CNOT, H, animate_circuit

anim = animate_circuit(
    initial_state=[1, 0, 0, 0],  # |00>
    gates=[(H, 0), CNOT],
    labels=[r"$H \otimes I$", "CNOT"],
    n_frames=50,
    interval=40,
    trail=True,
)

plt.suptitle(
    r"Bell state $|\Phi^+\rangle$ preparation",
    color="white",
    fontsize=13,
    y=1.01,
)
plt.tight_layout()
plt.show()
