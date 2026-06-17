"""Quantum state representation and Bloch vector computation."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from .gates import Gate, expand_gate

_SX: Gate = np.array([[0, 1], [1, 0]], dtype=complex)
_SY: Gate = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ: Gate = np.array([[1, 0], [0, -1]], dtype=complex)


class QuantumState:
    """Normalized quantum state with statevector or density matrix storage."""

    sv: npt.NDArray[np.complex128] | None
    n_qubits: int
    _rho: Gate

    def __init__(self, statevector: npt.ArrayLike) -> None:
        sv = np.array(statevector, dtype=complex)
        self.sv = sv / np.linalg.norm(sv)
        self.n_qubits = int(round(np.log2(len(sv))))
        self._rho = np.outer(self.sv, self.sv.conj())

    @classmethod
    def from_density_matrix(cls, rho: npt.ArrayLike) -> QuantumState:
        """Construct a state from a (possibly mixed) density matrix."""
        rho_arr = np.array(rho, dtype=complex)
        rho_arr = rho_arr / np.trace(rho_arr)
        obj = object.__new__(cls)
        obj.sv = None
        obj.n_qubits = int(round(np.log2(rho_arr.shape[0])))
        obj._rho = rho_arr
        return obj

    @classmethod
    def from_bloch_angles(cls, theta: float, phi: float) -> QuantumState:
        """Construct a pure state from Bloch sphere angles (theta, phi)."""
        sv = [np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)]
        return cls(sv)

    def bloch_vector(self, qubit_idx: int = 0) -> npt.NDArray[np.float64]:
        """Return (x, y, z) Bloch vector for qubit_idx via partial trace."""
        rho_q = _partial_trace(self._rho, qubit_idx, self.n_qubits)
        return np.array(
            [
                np.real(np.trace(rho_q @ _SX)),
                np.real(np.trace(rho_q @ _SY)),
                np.real(np.trace(rho_q @ _SZ)),
            ]
        )

    def apply(self, gate: Gate, target_qubit: int = 0) -> QuantumState:
        """Apply a gate to target_qubit and return a new QuantumState."""
        if gate.shape == (2**self.n_qubits, 2**self.n_qubits):
            U = gate
        else:
            U = expand_gate(gate, self.n_qubits, target_qubit)
        if self.sv is not None:
            return QuantumState(U @ self.sv)
        new_rho = U @ self._rho @ U.conj().T
        return QuantumState.from_density_matrix(new_rho)


def _partial_trace(rho: Gate, qubit_idx: int, n_qubits: int) -> Gate:
    """Trace out all qubits except qubit_idx; return 2x2 density matrix."""
    dim = 2**n_qubits
    rho_q = np.zeros((2, 2), dtype=complex)
    for i in range(2):
        for j in range(2):
            for k in range(dim // 2):
                row = _insert_bit(k, qubit_idx, i, n_qubits)
                col = _insert_bit(k, qubit_idx, j, n_qubits)
                rho_q[i, j] += rho[row, col]
    return rho_q


def _insert_bit(k: int, pos: int, bit: int, n_qubits: int) -> int:
    shift = n_qubits - 1 - pos
    high = k >> shift
    low = k & ((1 << shift) - 1)
    return (high << (shift + 1)) | (bit << shift) | low


def zero() -> QuantumState:
    """Return the |0⟩ computational basis state."""
    return QuantumState([1, 0])


def one() -> QuantumState:
    """Return the |1⟩ computational basis state."""
    return QuantumState([0, 1])


def plus() -> QuantumState:
    """Return the |+⟩ = (|0⟩+|1⟩)/√2 state."""
    return QuantumState([1, 1])


def minus() -> QuantumState:
    """Return the |−⟩ = (|0⟩−|1⟩)/√2 state."""
    return QuantumState([1, -1])
