import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, "..")
from blochviz import H, Rz, animate_circuit

anim = animate_circuit(
    initial_state=[1, 0],
    gates=[H, Rz(np.pi / 4), H],
    labels=["H", "Rz(π/4)", "H"],
    n_frames=40,
    interval=40,
    trail=True,
)

plt.tight_layout()
plt.show()
