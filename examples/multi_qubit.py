import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "..")
from blochviz import CNOT, H, animate_circuit

# Bell state: |00⟩ → (H⊗I) → CNOT → |Φ+⟩
# H on qubit 0, then CNOT (full 4x4 matrix)
anim = animate_circuit(
    initial_state=[1, 0, 0, 0],  # |00⟩
    gates=[(H, 0), CNOT],
    labels=["H ⊗ I", "CNOT"],
    n_frames=50,
    interval=40,
    trail=True,
)

plt.suptitle("Bell state |Φ+⟩ preparation", color="white", fontsize=13, y=1.01)
plt.tight_layout()
plt.show()
