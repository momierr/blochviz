from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure

from .gates import Gate
from .sphere import BlochSphere
from .state import QuantumState

GateSpec = Gate | tuple[Gate, int]


def _slerp(
    v0: npt.NDArray[np.float64], v1: npt.NDArray[np.float64], t: float
) -> npt.NDArray[np.float64]:
    """Spherical linear interpolation between two vectors."""
    v0 = np.array(v0, dtype=float)
    v1 = np.array(v1, dtype=float)
    dot = np.clip(
        np.dot(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1) + 1e-12), -1, 1
    )
    omega = np.arccos(dot)
    if omega < 1e-10:
        return np.asarray(v0 + t * (v1 - v0), dtype=np.float64)
    return np.asarray(
        (np.sin((1 - t) * omega) * v0 + np.sin(t * omega) * v1) / np.sin(omega),
        dtype=np.float64,
    )


def animate_circuit(
    initial_state: QuantumState | npt.ArrayLike,
    gates: list[GateSpec],
    labels: list[str] | None = None,
    n_frames: int = 30,
    interval: int = 50,
    trail: bool = True,
    figsize: tuple[float, float] | None = None,
) -> FuncAnimation:
    """
    Animate a sequence of quantum gates on the Bloch sphere.

    Parameters
    ----------
    initial_state : QuantumState or array-like
        Statevector, e.g. [1, 0] for |0> or [1, 0, 0, 0] for |00>.
    gates : list of Gate or (Gate, target_qubit)
        Each element is a gate matrix or a (gate, target_qubit) tuple.
    labels : list of str, optional
        Gate label for each step, shown in figure title.
    n_frames : int
        Interpolation frames between gate steps.
    interval : int
        Milliseconds between frames.
    trail : bool
        Draw trajectory trail on sphere.

    Returns
    -------
    FuncAnimation
    """
    if not isinstance(initial_state, QuantumState):
        initial_state = QuantumState(initial_state)
    state = initial_state
    n_qubits = state.n_qubits
    if labels is None:
        labels = [f"Gate {i + 1}" for i in range(len(gates))]

    states = [state]
    for g in gates:
        if isinstance(g, tuple):
            gate_mat, target = g
        else:
            gate_mat, target = g, 0
        state = state.apply(gate_mat, target)
        states.append(state)

    bloch_seqs: list[list[npt.NDArray[np.float64]]] = [
        [s.bloch_vector(q) for s in states] for q in range(n_qubits)
    ]

    frame_bloch: list[list[npt.NDArray[np.float64]]] = []
    frame_labels: list[str] = []

    for step_idx, label in enumerate(labels):
        v_start = [bloch_seqs[q][step_idx] for q in range(n_qubits)]
        v_end = [bloch_seqs[q][step_idx + 1] for q in range(n_qubits)]
        for f in range(n_frames):
            t = f / (n_frames - 1) if n_frames > 1 else 1.0
            frame_bloch.append(
                [_slerp(v_start[q], v_end[q], t) for q in range(n_qubits)]
            )
            frame_labels.append(label)

    if figsize is None:
        figsize = (4 * n_qubits, 4.5)
    fig = plt.figure(figsize=figsize, facecolor="black")

    spheres: list[BlochSphere] = []
    for q in range(n_qubits):
        ax = fig.add_subplot(1, n_qubits, q + 1, projection="3d")
        spheres.append(BlochSphere(ax, title=f"qubit {q}"))

    title_text = fig.suptitle("", color="white", fontsize=12, y=0.98)

    def init() -> list[Any]:
        for q, sphere in enumerate(spheres):
            sphere.reset_trail()
            sphere.update(bloch_seqs[q][0], trail=False)
        title_text.set_text("Initial state")
        return []

    def update(frame: int) -> list[Any]:
        vecs = frame_bloch[frame]
        label = frame_labels[frame]
        for q, sphere in enumerate(spheres):
            sphere.update(vecs[q], trail=trail)
        title_text.set_text(label)
        return []

    return FuncAnimation(
        fig,
        update,
        frames=len(frame_bloch),
        init_func=init,
        interval=interval,
        blit=False,
    )


def plot_state(
    state: QuantumState | npt.ArrayLike,
    qubit_idx: int = 0,
    title: str = "",
    figsize: tuple[float, float] = (4, 4.5),
) -> Figure:
    """Render a single quantum state as a static Bloch sphere."""
    if not isinstance(state, QuantumState):
        state = QuantumState(state)
    fig = plt.figure(figsize=figsize, facecolor="black")
    ax = fig.add_subplot(111, projection="3d")
    sphere = BlochSphere(ax, title=title)
    sphere.update(state.bloch_vector(qubit_idx), trail=False)
    return fig


def save_animation(
    anim: FuncAnimation, path: str, fps: int = 25, dpi: int = 100
) -> None:
    """Save an animation to .gif (Pillow) or .mp4 (ffmpeg) based on file extension."""
    ext = path.rsplit(".", 1)[-1].lower()
    writer = "pillow" if ext == "gif" else "ffmpeg"
    anim.save(path, writer=writer, fps=fps, dpi=dpi)
