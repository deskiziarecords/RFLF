# src/rflf/utils.py
"""Utility helpers for RFLF."""

def exponential_kernel(delta, t):
    """
    Exponential memory kernel:
    
    $$
    K(t) = \\exp(-\\delta t)
    $$

    Parameters
    ----------
    delta : float
        Decay rate.
    t : array_like
        Time vector.

    Returns
    -------
    np.ndarray
        Kernel values.
    """
    return np.exp(-delta * t)
