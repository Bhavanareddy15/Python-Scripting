"""Visualization helpers: plot a sorted polygon, with or without holes."""

import matplotlib.pyplot as plt


def _draw_loop(ax, ordered_points, color, start_marker=False):
    xs = [p[0] for p in ordered_points] + [ordered_points[0][0]]
    ys = [p[1] for p in ordered_points] + [ordered_points[0][1]]
    ax.plot(xs, ys, '-o', color=color, linewidth=1.5, markersize=5)
    for i, (x, y) in enumerate(ordered_points):
        ax.annotate(str(i), (x, y), textcoords="offset points",
                    xytext=(8, 8), fontsize=9, color=color)
    if start_marker:
        sx, sy = ordered_points[0]
        ax.plot(sx, sy, 'o', color='#D85A30', markersize=10, zorder=5)
        ax.annotate("start", (sx, sy), textcoords="offset points",
                    xytext=(8, -14), fontsize=10, color='#993C1D')


def plot_sorted_polygon(ordered_points, title="Sorted polygon", save_path=None):
    """Plots a single simple polygon (no holes)."""
    fig, ax = plt.subplots(figsize=(6, 6))
    _draw_loop(ax, ordered_points, color='#1D9E75', start_marker=True)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fig


def plot_polygon_with_holes(result, title="Sorted polygon", save_path=None):
    """
    Plots the output of sort_rectilinear_polygon_with_holes:
    {'outer': [...], 'holes': [[...], ...]}.
    Outer boundary in teal (solid), holes in orange.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    _draw_loop(ax, result['outer'], color='#1D9E75', start_marker=True)
    for hole in result['holes']:
        _draw_loop(ax, hole, color='#D85A30', start_marker=False)
    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return fig