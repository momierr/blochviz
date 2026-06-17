import numpy as np

from .gates import expand_gate

_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)


class QuantumState:
    def __init__(self, statevector):
        sv = np.array(statevector, dtype=complex)
        self.sv = sv / np.linalg.norm(sv)
        self.n_qubits = int(round(np.log2(len(sv))))
        self._rho = np.outer(self.sv, self.sv.conj())

    @classmethod
    def from_density_matrix(cls, rho):
        rho = np.array(rho, dtype=complex)
        rho = rho / np.trace(rho)
        obj = object.__new__(cls)
        obj.sv = None
        obj.n_qubits = int(round(np.log2(rho.shape[0])))
        obj._rho = rho
        return obj

    @classmethod
    def from_bloch_angles(cls, theta, phi):
        """Pure state from Bloch sphere polar angles theta ∈ [0,π], phi ∈ [0,2π)."""
        sv = [np.cos(theta / 2), np.exp(1j * phi) * np.sin(theta / 2)]
        return cls(sv)

    def bloch_vector(self, qubit_idx=0):
        """(x, y, z) Bloch vector for qubit_idx via partial trace of the density matrix."""
        rho_q = _partial_trace(self._rho, qubit_idx, self.n_qubits)
        return np.array(
            [
                np.real(np.trace(rho_q @ _SX)),
                np.real(np.trace(rho_q @ _SY)),
                np.real(np.trace(rho_q @ _SZ)),
            ]
        )

    def apply(self, gate, target_qubit=0):
        if gate.shape == (2**self.n_qubits, 2**self.n_qubits):
            U = gate
        else:
            U = expand_gate(gate, self.n_qubits, target_qubit)
        if self.sv is not None:
            return QuantumState(U @ self.sv)
        new_rho = U @ self._rho @ U.conj().T
        return QuantumState.from_density_matrix(new_rho)


def _partial_trace(rho, qubit_idx, n_qubits):
    """Trace out all qubits except qubit_idx, return 2x2 reduced density matrix."""
    dim = 2**n_qubits
    rho_q = np.zeros((2, 2), dtype=complex)
    for i in range(2):
        for j in range(2):
            for k in range(dim // 2):
                row = _insert_bit(k, qubit_idx, i, n_qubits)
                col = _insert_bit(k, qubit_idx, j, n_qubits)
                rho_q[i, j] += rho[row, col]
    return rho_q


def _insert_bit(k, pos, bit, n_qubits):
    shift = n_qubits - 1 - pos
    high = k >> shift
    low = k & ((1 << shift) - 1)
    return (high << (shift + 1)) | (bit << shift) | low


# Convenience constructors
def zero():
    return QuantumState([1, 0])


def one():
    return QuantumState([0, 1])


def plus():
    return QuantumState([1, 1])


def minus():
    return QuantumState([1, -1])
