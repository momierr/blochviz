import numpy as np
import pytest

from blochviz import CNOT, H, QuantumState, X, minus, one, plus, zero


def test_zero_bloch():
    assert np.allclose(zero().bloch_vector(), [0, 0, 1])


def test_one_bloch():
    assert np.allclose(one().bloch_vector(), [0, 0, -1])


def test_plus_bloch():
    assert np.allclose(plus().bloch_vector(), [1, 0, 0])


def test_minus_bloch():
    assert np.allclose(minus().bloch_vector(), [-1, 0, 0])


def test_apply_hadamard():
    assert np.allclose(zero().apply(H).bloch_vector(), [1, 0, 0])


def test_apply_x():
    assert np.allclose(zero().apply(X).bloch_vector(), [0, 0, -1])


def test_from_bloch_angles_plus():
    s = QuantumState.from_bloch_angles(np.pi / 2, 0)
    assert np.allclose(s.bloch_vector(), [1, 0, 0], atol=1e-6)


def test_from_bloch_angles_poles():
    assert np.allclose(QuantumState.from_bloch_angles(0, 0).bloch_vector(), [0, 0, 1])
    assert np.allclose(
        QuantumState.from_bloch_angles(np.pi, 0).bloch_vector(), [0, 0, -1], atol=1e-6
    )


def test_density_matrix_pure():
    rho = np.array([[1, 0], [0, 0]], dtype=complex)
    s = QuantumState.from_density_matrix(rho)
    assert np.allclose(s.bloch_vector(), [0, 0, 1])


def test_density_matrix_mixed():
    rho = np.eye(2, dtype=complex) / 2
    s = QuantumState.from_density_matrix(rho)
    assert np.allclose(s.bloch_vector(), [0, 0, 0])


def test_density_matrix_apply():
    rho = np.array([[1, 0], [0, 0]], dtype=complex)
    s = QuantumState.from_density_matrix(rho).apply(H)
    assert np.allclose(s.bloch_vector(), [1, 0, 0], atol=1e-6)


def test_bell_state_entanglement():
    s = QuantumState([1, 0, 0, 0]).apply(H, 0).apply(CNOT)
    # Both reduced states must be maximally mixed → zero Bloch vector
    assert np.allclose(s.bloch_vector(0), [0, 0, 0], atol=1e-6)
    assert np.allclose(s.bloch_vector(1), [0, 0, 0], atol=1e-6)


def test_normalization():
    s = QuantumState([3, 4])
    assert np.isclose(np.linalg.norm(s.bloch_vector()), 1.0, atol=1e-6)
