# tests/test_core.py
import numpy as np
from src.rflf.core import RFLFSystem
from src.rflf.utils import exponential_kernel

def test_basic_integration():
    # Linear forward dynamics: ds/dt = -s
    def F(s, t): return -s

    # Simple proportional feedback: G = 0.1 * s
    def G(s, _): return 0.1 * s

    # Exponential memory kernel with decay 0.5
    def K(tau): return exponential_kernel(delta=0.5, t=tau)

    # Noise term
    def eta(t, s): return np.random.randn(*s.shape) * 0.01

    system = RFLFSystem(F=F, G=G, K=K, eta=eta)
    sol = system.integrate(t_span=(0, 10), s0=np.array([1.0, 0.0]), dense_output=False)

    assert sol.t.size > 1
    assert sol.y.shape[1] == 2
