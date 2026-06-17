"""2-qubit Grover search for |11⟩. One iteration → probability 1."""

import matplotlib.pyplot as plt

from blochviz import CZ, H, X, animate_circuit

# Oracle: CZ marks |11⟩ with a phase flip
# Diffusion: H⊗H → X⊗X → CZ → X⊗X → H⊗H
gates = [
    (H, 0),
    (H, 1),  # uniform superposition
    CZ,  # oracle: phase flip |11⟩
    (H, 0),
    (H, 1),  # diffusion step 1
    (X, 0),
    (X, 1),  # diffusion step 2
    CZ,  # phase flip |00⟩ (= |11⟩ after X)
    (X, 0),
    (X, 1),  # diffusion step 3
    (H, 0),
    (H, 1),  # diffusion step 4 → |11⟩
]
labels = [
    "H⊗I",
    "I⊗H",
    "Oracle (CZ)",
    "H⊗I",
    "I⊗H",
    "X⊗I",
    "I⊗X",
    "Phase flip |00⟩",
    "X⊗I",
    "I⊗X",
    "H⊗I",
    "I⊗H",
]

anim = animate_circuit(
    initial_state=[1, 0, 0, 0],
    gates=gates,
    labels=labels,
    n_frames=30,
    interval=50,
    trail=True,
)

plt.suptitle("Grover search: |11⟩  (2 qubits, 1 iteration)", color="white", fontsize=12)
plt.tight_layout()
plt.show()
