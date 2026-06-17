from __future__ import annotations

import numpy as np
import numpy.typing as npt

Gate = npt.NDArray[np.complex128]

I: Gate = np.eye(2, dtype=complex)  # noqa: E741
X: Gate = np.array([[0, 1], [1, 0]], dtype=complex)
Y: Gate = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z: Gate = np.array([[1, 0], [0, -1]], dtype=complex)
H: Gate = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
S: Gate = np.array([[1, 0], [0, 1j]], dtype=complex)
T: Gate = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

CNOT: Gate = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)

CZ: Gate = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, -1],
    ],
    dtype=complex,
)


def Rx(theta: float) -> Gate:
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -1j * s], [-1j * s, c]], dtype=complex)


def Ry(theta: float) -> Gate:
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def Rz(theta: float) -> Gate:
    return np.array(
        [[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]], dtype=complex
    )


def expand_gate(U: Gate, n_qubits: int, target: int) -> Gate:
    """Embed a 2x2 gate U acting on `target` qubit into a 2^n x 2^n matrix."""
    ops: list[Gate] = [U if i == target else I for i in range(n_qubits)]
    result: Gate = ops[0]
    for op in ops[1:]:
        result = np.asarray(np.kron(result, op), dtype=np.complex128)
    return result
