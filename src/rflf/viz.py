# src/rflf/viz.py
"""Visualization utilities."""

import matplotlib.pyplot as plt

def plot_trajectory(t, y, title="RFLF Trajectory"):
    """
    Plot state trajectory over time.
    
    Parameters
    ----------
    t : array_like
        Time points.
    y : array_like
        State trajectory (shape `[n_states, len(t)]`).
    """
    plt.figure(figsize=(8, 4))
    for i in range(y.shape[0]):
        plt.plot(t, y[i, :], label=f"state {i+1}")
    plt.xlabel("Time $t$")
    plt.ylabel("State")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
