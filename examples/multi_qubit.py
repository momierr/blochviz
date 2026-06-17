"""Entanglement cycle: create a Bell state then disentangle back to |00>."""

import matplotlib.pyplot as plt

from blochviz import CNOT, H, animate_circuit

# H(x)I puts qubit 0 in superposition (product state: spheres on poles/equator).
# CNOT entangles: both reduced states become maximally mixed -> spheres collapse
# to the origin. A second CNOT + H unwinds the entanglement back to |00>.
gates = [
    (H, 0),
    CNOT,
    CNOT,
    (H, 0),
]
labels = [
    r"$H \otimes I$: superposition, still a product state",
    "CNOT: entangle  ->  both qubits collapse to the origin!",
    "CNOT: disentangle  ->  product state restored",
    r"$H \otimes I$: recover $|00\rangle$",
]

anim = animate_circuit(
    initial_state=[1, 0, 0, 0],
    gates=gates,
    labels=labels,
    n_frames=60,
    interval=40,
    trail=True,
)

plt.suptitle(
    r"Entanglement: $|00\rangle \to |\Phi^+\rangle \to |00\rangle$",
    color="white",
    fontsize=13,
)
plt.tight_layout()
plt.show()
