import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from .sphere import BlochSphere
from .state import QuantumState


def _slerp(v0, v1, t):
    """Spherical linear interpolation between two vectors."""
    v0 = np.array(v0, dtype=float)
    v1 = np.array(v1, dtype=float)
    dot = np.clip(
        np.dot(v0, v1) / (np.linalg.norm(v0) * np.linalg.norm(v1) + 1e-12), -1, 1
    )
    omega = np.arccos(dot)
    if omega < 1e-10:
        return v0 + t * (v1 - v0)
    return (np.sin((1 - t) * omega) * v0 + np.sin(t * omega) * v1) / np.sin(omega)


def animate_circuit(
    initial_state,
    gates,
    labels=None,
    n_frames=30,
    interval=50,
    trail=True,
    figsize=None,
):
    """
    Animate a sequence of quantum gates on the Bloch sphere.

    Parameters
    ----------
    initial_state : array-like
        Statevector, e.g. [1, 0] for |0⟩ or [1, 0, 0, 0] for |00⟩.
    gates : list
        Each element is either:
        - a 2D numpy array (gate matrix), applied to qubit 0 for 1-qubit circuits,
          or a full 2^n x 2^n matrix for n-qubit circuits
        - a tuple (gate_matrix, target_qubit)
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
    matplotlib.animation.FuncAnimation
    """
    if not isinstance(initial_state, QuantumState):
        initial_state = QuantumState(initial_state)
    state = initial_state
    n_qubits = state.n_qubits
    if labels is None:
        labels = [f"Gate {i + 1}" for i in range(len(gates))]

    # Build sequence of states: initial + one per gate
    states = [state]
    parsed_gates = []
    for g in gates:
        if isinstance(g, tuple):
            gate_mat, target = g
        else:
            gate_mat, target = g, 0
        state = state.apply(gate_mat, target)
        states.append(state)
        parsed_gates.append((gate_mat, target))

    # Pre-compute Bloch vectors for every qubit at every state
    bloch_seqs = []  # bloch_seqs[qubit][step] = (x,y,z)
    for q in range(n_qubits):
        bloch_seqs.append([s.bloch_vector(q) for s in states])

    # Build frame list: for each gate, n_frames interpolated Bloch vectors per qubit
    # frames[frame_idx] = list of bloch_vec per qubit
    frame_bloch = []  # list of [vec_q0, vec_q1, ...]
    frame_labels = []

    for step_idx, label in enumerate(labels):
        v_start = [bloch_seqs[q][step_idx] for q in range(n_qubits)]
        v_end = [bloch_seqs[q][step_idx + 1] for q in range(n_qubits)]
        for f in range(n_frames):
            t = f / (n_frames - 1) if n_frames > 1 else 1.0
            frame_bloch.append(
                [_slerp(v_start[q], v_end[q], t) for q in range(n_qubits)]
            )
            frame_labels.append(label)

    # Set up figure
    if figsize is None:
        figsize = (4 * n_qubits, 4.5)
    fig = plt.figure(figsize=figsize, facecolor="black")

    axes = []
    spheres = []
    qubit_titles = [f"qubit {q}" for q in range(n_qubits)]
    for q in range(n_qubits):
        ax = fig.add_subplot(1, n_qubits, q + 1, projection="3d")
        axes.append(ax)
        spheres.append(BlochSphere(ax, title=qubit_titles[q]))

    title_text = fig.suptitle("", color="white", fontsize=12, y=0.98)

    def init():
        for q, sphere in enumerate(spheres):
            sphere.reset_trail()
            sphere.update(bloch_seqs[q][0], trail=False)
        title_text.set_text("Initial state")
        return []

    def update(frame):
        vecs = frame_bloch[frame]
        label = frame_labels[frame]
        for q, sphere in enumerate(spheres):
            sphere.update(vecs[q], trail=trail)
        title_text.set_text(label)
        return []

    anim = FuncAnimation(
        fig,
        update,
        frames=len(frame_bloch),
        init_func=init,
        interval=interval,
        blit=False,
    )
    return anim


def plot_state(state, qubit_idx=0, title="", figsize=(4, 4.5)):
    """Render a single quantum state as a static Bloch sphere.

    Parameters
    ----------
    state : QuantumState or array-like
        State to render.
    qubit_idx : int
        Which qubit to visualize (for multi-qubit states).
    title : str
        Subplot title.
    figsize : tuple

    Returns
    -------
    matplotlib.figure.Figure
    """
    if not isinstance(state, QuantumState):
        state = QuantumState(state)
    fig = plt.figure(figsize=figsize, facecolor="black")
    ax = fig.add_subplot(111, projection="3d")
    sphere = BlochSphere(ax, title=title)
    sphere.update(state.bloch_vector(qubit_idx), trail=False)
    return fig


def save_animation(anim, path, fps=25, dpi=100):
    """Save an animation returned by animate_circuit().

    Parameters
    ----------
    anim : FuncAnimation
    path : str
        Output path. Extension determines format: .gif uses Pillow, .mp4 uses ffmpeg.
    fps : int
    dpi : int
    """
    ext = path.rsplit(".", 1)[-1].lower()
    writer = "pillow" if ext == "gif" else "ffmpeg"
    anim.save(path, writer=writer, fps=fps, dpi=dpi)
