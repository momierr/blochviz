# blochviz

Minimal Bloch sphere visualizer. Single and multi-qubit states, animated gate sequences, matplotlib only.

## Install

```bash
pip install -e .
```

## Quick start

```python
from blochviz import animate_circuit, H, Rz
import numpy as np
import matplotlib.pyplot as plt

anim = animate_circuit(
    initial_state=[1, 0],          # |0⟩
    gates=[H, Rz(np.pi / 4), H],
    labels=["H", "Rz(π/4)", "H"],
)
plt.show()
```

## API

### `animate_circuit(initial_state, gates, ...)`

Animate a gate sequence on the Bloch sphere. Returns a `FuncAnimation`.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `initial_state` | — | Statevector `[1,0]` or `QuantumState` |
| `gates` | — | List of gate matrices or `(gate, target_qubit)` tuples |
| `labels` | auto | Gate labels shown in title |
| `n_frames` | 30 | Interpolation frames per gate |
| `interval` | 50 | ms between frames |
| `trail` | True | Draw trajectory trail |

Multi-qubit: pass a `2^n` statevector and use `(gate, target_qubit)` tuples or full `2^n × 2^n` matrices.

### `plot_state(state, qubit_idx=0, title="")`

Static Bloch sphere snapshot. Returns a `Figure`.

### `save_animation(anim, path, fps=25, dpi=100)`

Save to `.gif` (Pillow) or `.mp4` (ffmpeg).

```python
save_animation(anim, "circuit.gif")
```

### State constructors

```python
from blochviz import zero, one, plus, minus, QuantumState

QuantumState([1, 0])                        # from statevector
QuantumState.from_bloch_angles(theta, phi)  # from Bloch angles
QuantumState.from_density_matrix(rho)       # from density matrix (pure or mixed)
zero()   # |0⟩    one()   # |1⟩
plus()   # |+⟩    minus() # |−⟩
```

### Gates

```python
from blochviz import I, X, Y, Z, H, S, T, CNOT, CZ, Rx, Ry, Rz
```

`Rx(θ)`, `Ry(θ)`, `Rz(θ)` are factories returning 2×2 matrices.

## Examples

| File | What it shows |
|------|--------------|
| `examples/single_qubit.py` | H → Rz(π/4) → H |
| `examples/phase_gates.py` | T⁸ = I: full Z-rotation via phase gates |
| `examples/state_sweep.py` | Ry sweep: \|0⟩ → \|1⟩ along the meridian |
| `examples/multi_qubit.py` | Bell state \|Φ⁺⟩ preparation |
| `examples/grover.py` | 2-qubit Grover search for \|11⟩ |

```bash
cd examples
python phase_gates.py
python grover.py
```

## Tests

```bash
pytest -v
```

## Notes

- Multi-qubit Bloch spheres show **reduced** (per-qubit) states via partial trace. Entangled qubits appear as vectors inside the sphere (length < 1), with the maximally entangled Bell state giving a zero-length vector — a direct visual of entanglement.
- No scipy, no QuTiP. Pure numpy + matplotlib.
