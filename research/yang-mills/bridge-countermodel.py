"""Four-state spectral countermodel: local decay does not force a global gap.
This is generic finite-dimensional mathematics, not native NEW K or Yang–Mills.
Requires NumPy.
"""
import numpy as np

def local_decay_rate_and_gap(n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    h = np.kron(np.diag([0., 1.]), np.eye(2)) + np.kron(np.eye(2), np.diag([0., 1. / n]))
    omega = np.array([1., 0., 0., 0.])
    sigma_x = np.array([[0., 1.], [1., 0.]])
    psi = np.kron(sigma_x, np.eye(2)) @ omega
    rate = float(psi @ h @ psi)
    if not np.allclose(h @ psi, rate * psi, atol=1e-12):
        raise ArithmeticError("local excitation is not an eigenvector")
    return rate, float(np.linalg.eigvalsh(h)[1])

if __name__ == "__main__":
    for n in (2, 10, 1000):
        rate, gap = local_decay_rate_and_gap(n)
        assert abs(rate - 1.) < 1e-12 and abs(gap - 1. / n) < 1e-12
        print(f"n={n}: local_rate={rate:g}, global_gap={gap:g}")
