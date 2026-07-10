import math
import matplotlib.pyplot as plt


def sort_star_shaped_polygon(points):
    """
    Sort vertices of a star-shaped polygon starting from the
    bottom-left-most point, proceeding counter-clockwise.

    Assumptions:
      - points form a simple, star-shaped polygon
      - standard math coordinates (y increases upward)
      - 'bottom-left-most' = smallest x, tie-broken by smallest y
        (i.e. leftmost first, then bottommost among ties)
      - the vertex average (centroid) lies within the polygon's kernel
        (holds for symmetric/compact star shapes like a plus sign;
        not guaranteed for arbitrary star-shaped polygons)
    """
    if len(points) < 3:
        raise ValueError("Need at least 3 points to form a polygon")

    # 1. Starting vertex: leftmost first, then bottommost among ties
    start = min(points, key=lambda p: (p[0], p[1]))

    # 2. Centroid approximation (vertex average)
    cx = sum(p[0] for p in points) / len(points)
    cy = sum(p[1] for p in points) / len(points)

    # 3. Sort by angle from centroid (CCW), tie-break by distance
    #    to handle points that fall on the same ray from the centroid
    def sort_key(p):
        angle = math.atan2(p[1] - cy, p[0] - cx)
        dist = math.hypot(p[0] - cx, p[1] - cy)
        return (angle, dist)

    ordered = sorted(points, key=sort_key)

    # 4. Rotate so the list starts at `start`
    start_idx = ordered.index(start)
    ordered = ordered[start_idx:] + ordered[:start_idx]

    return ordered


def plot_sorted_polygon(ordered_points, title="Sorted polygon", save_path=None):
    """Plot the polygon boundary with vertices numbered in traversal order."""
    xs = [p[0] for p in ordered_points] + [ordered_points[0][0]]
    ys = [p[1] for p in ordered_points] + [ordered_points[0][1]]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xs, ys, '-o', color='#1D9E75', linewidth=1.5, markersize=5)

    # number each vertex in traversal order
    for i, (x, y) in enumerate(ordered_points):
        ax.annotate(str(i), (x, y), textcoords="offset points",
                    xytext=(8, 8), fontsize=10, color='#0F6E56')

    # mark the starting point distinctly
    sx, sy = ordered_points[0]
    ax.plot(sx, sy, 'o', color='#D85A30', markersize=10, zorder=5)
    ax.annotate("start", (sx, sy), textcoords="offset points",
                xytext=(8, -14), fontsize=10, color='#993C1D')

    ax.set_title(title)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.3)

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


if __name__ == "__main__":
    pts = [(5, 2), (5, 3), (2, 3), (0, 3), (2, 2), (3, 5), (3, 2),
           (2, 0), (0, 2), (3, 3), (2, 5), (3, 0)]

    result = sort_star_shaped_polygon(pts)
    print("Sorted order:", result)

    plot_sorted_polygon(result, title="Plus-shape: sorted CCW from leftmost-bottommost point",
                         save_path="plus_shape_sorted.png")