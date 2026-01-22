# src/rflf/core.py
"""Core implementation of the RFLF engine."""

import numpy as np
from scipy.integrate import solve_ivp

class RFLFSystem:
    """
    Build a Recursive Feedback Loop System.
    
    Parameters
    ----------
    F : callable
        Forward evolution function $F(st, t)$.
    G : callable
        Feedback function $G(s, H(s))$.
    K : callable
        Memory kernel $K(t-\tau)$.
    eta : callable, optional
        Noise/perturbation function $\eta(t)$.
    """

    def __init__(self, F, G, K, eta=None):
        self.F = F
        self.G = G
        self.K = K
        self.eta = eta or (lambda t, s: np.zeros_like(s))

    def _memory_integral(self, t, s):
        """Compute $\\int_{0}^{t} K(t-\\tau) G(s(\\tau)) d\\tau$."""
        # Simple trapezoidal rule over a dense grid
        eps = 0.01
        tau_grid = np.arange(0, t+eps, eps)
        kernel = self.K(t - tau_grid)
        # Assume `self._history` holds past states – placeholder for brevity
        past_output = self.G(s, None)  # replace with actual history when needed
        integral = np.trapz(kernel * past_output, dx=eps)
        return integral

    def rhs(self, t, s):
        """
        Right‑hand side of the unified RFLF equation:
        
        $$
        \\frac{\\partial s}{\\partial t}=F(s,t)+\\int_{0}^{t}K(t-\\tau)G(s(\\tau))d\\tau+\\eta(t)
        $$
        """
        forward = self.F(s, t)
        memory  = self._memory_integral(t, s)
        noise   = self.eta(t, s)
        return forward + memory + noise

    def integrate(self, t_span, s0, **kwargs):
        """
        Numerically integrate the system.
        
        Parameters
        ----------
        t_span : tuple
            `(t0, tf)` integration interval.
        s0 : array_like
            Initial state vector.
        kwargs : dict
            Additional arguments passed to `solve_ivp`.

        Returns
        -------
        sol : Bunch
            Result object with `.t` and `.y` attributes.
        """
        sol = solve_ivp(
            fun=lambda t, y: self.rhs(t, y),
            t_span=t_span,
            y0=s0,
            **kwargs
        )
        return sol
