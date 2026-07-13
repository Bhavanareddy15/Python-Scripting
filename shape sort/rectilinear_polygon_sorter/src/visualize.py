"""Visualization helper: plots a sorted polygon with numbered vertices."""

import matplotlib.pyplot as plt


def plot_sorted_polygon(ordered_points, title="Sorted polygon", save_path=None):
    xs = [p[0] for p in ordered_points] + [ordered_points[0][0]]
    ys = [p[1] for p in ordered_points] + [ordered_points[0][1]]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xs, ys, '-o', color='#1D9E75', linewidth=1.5, markersize=5)

    for i, (x, y) in enumerate(ordered_points):
        ax.annotate(str(i), (x, y), textcoords="offset points",
                    xytext=(8, 8), fontsize=10, color='#0F6E56')

    sx, sy = ordered_points[0]
    ax.plot(sx, sy, 'o', color='#D85A30', markersize=10, zorder=5)
    ax.annotate("start", (sx, sy), textcoords="offset points",
                xytext=(8, -14), fontsize=10, color='#993C1D')

    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fig
