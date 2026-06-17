import numpy as np
import pytest

from blochviz import CNOT, CZ, H, I, Rx, Ry, Rz, S, T, X, Y, Z
from blochviz.gates import expand_gate


@pytest.mark.parametrize("G", [X, Y, Z, H, S, T, CNOT, CZ])
def test_unitarity(G):
    n = G.shape[0]
    assert np.allclose(G @ G.conj().T, np.eye(n), atol=1e-12)


@pytest.mark.parametrize("theta", [0, np.pi / 4, np.pi / 2, np.pi, 2 * np.pi])
@pytest.mark.parametrize("factory", [Rx, Ry, Rz])
def test_rotation_unitarity(factory, theta):
    G = factory(theta)
    assert np.allclose(G @ G.conj().T, np.eye(2), atol=1e-12)


def test_rx_pi():
    result = Rx(np.pi) @ np.array([1, 0], dtype=complex)
    assert np.allclose(result, [0, -1j], atol=1e-12)


def test_ry_pi():
    result = Ry(np.pi) @ np.array([1, 0], dtype=complex)
    assert np.allclose(result, [0, 1], atol=1e-12)


def test_rz_pi():
    result = Rz(np.pi) @ np.array([1, 0], dtype=complex)
    assert np.allclose(result, [np.exp(-1j * np.pi / 2), 0], atol=1e-12)


def test_expand_gate_qubit0():
    U = expand_gate(X, 2, 0)
    assert np.allclose(U, np.kron(X, I))


def test_expand_gate_qubit1():
    U = expand_gate(X, 2, 1)
    assert np.allclose(U, np.kron(I, X))


def test_t_gate_eighth_root():
    # T^8 = I (global phase aside)
    T8 = np.linalg.matrix_power(T, 8)
    assert np.allclose(T8, np.eye(2), atol=1e-12)


def test_hadamard_involutory():
    assert np.allclose(H @ H, np.eye(2), atol=1e-12)
