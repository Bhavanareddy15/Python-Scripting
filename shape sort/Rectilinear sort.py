from collections import defaultdict
import matplotlib.pyplot as plt


def reconstruct_rectilinear_polygon(points):
    """
    Reconstruct the boundary order of a simple, axis-aligned (rectilinear)
    polygon from an unordered point set.

    Method: even-odd parity rule. Group points sharing an x (or y)
    coordinate, sort by the other coordinate, and pair them up
    (1st-2nd, 3rd-4th, ...) as real boundary edges -- a line through a
    simple polygon must cross its boundary an even number of times,
    alternating inside/outside. This holds for ANY simple orthogonal
    polygon; no star-shaped / line-of-sight assumption needed.

    Starts at the leftmost point (ties broken by smallest y), and walks
    the reconstructed boundary counter-clockwise.
    """
    if len(points) < 4:
        raise ValueError("Need at least 4 points for a rectilinear polygon")

    by_x = defaultdict(list)
    by_y = defaultdict(list)
    for p in points:
        by_x[p[0]].append(p)
        by_y[p[1]].append(p)

    print(by_x)
    print(by_y)  
    

    adjacency = defaultdict(list)

    for x, group in by_x.items():
        group.sort(key=lambda p: p[1])
        if len(group) % 2 != 0:
            raise ValueError(f"Odd number of points at x={x}; not a valid "
                              f"simple rectilinear polygon")
        for i in range(0, len(group), 2):
            a, b = group[i], group[i + 1]
            adjacency[a].append(b)
            adjacency[b].append(a)

    for y, group in by_y.items():
        group.sort(key=lambda p: p[0])
        if len(group) % 2 != 0:
            raise ValueError(f"Odd number of points at y={y}; not a valid "
                              f"simple rectilinear polygon")
        for i in range(0, len(group), 2):
            a, b = group[i], group[i + 1]
            adjacency[a].append(b)
            adjacency[b].append(a)

    for p, neighbors in adjacency.items():
        if len(neighbors) != 2:
            raise ValueError(f"Point {p} has {len(neighbors)} edges instead "
                              f"of 2 -- input is ambiguous or not a valid "
                              f"simple rectilinear polygon")

    start = min(points, key=lambda p: (p[0], p[1]))
    ordered = [start]
    prev, cur = None, start
    while True:
        n1, n2 = adjacency[cur]
        nxt = n1 if n1 != prev else n2
        if nxt == start:
            break
        ordered.append(nxt)
        prev, cur = cur, nxt

    if len(ordered) != len(points):
        raise ValueError("Reconstructed cycle doesn't include every point -- "
                          "input may describe more than one disconnected shape")

    area = _signed_area(ordered)
    if area < 0:
        ordered = [ordered[0]] + ordered[1:][::-1]

    return ordered


def _signed_area(points):
    n = len(points)
    return sum(points[i][0] * points[(i + 1) % n][1] -
               points[(i + 1) % n][0] * points[i][1]
               for i in range(n)) / 2


def _segments_intersect(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = ccw(p3, p4, p1), ccw(p3, p4, p2)
    d3, d4 = ccw(p1, p2, p3), ccw(p1, p2, p4)
    return ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0))


def validate_simple_polygon(ordered_points):
    """
    Safety-net check: confirms no two non-adjacent edges cross.
    Returns (is_valid: bool, message: str).
    Catches cases the parity-pairing rule could get wrong on
    degenerate/ambiguous rectilinear layouts.
    """
    n = len(ordered_points)
    edges = [(ordered_points[i], ordered_points[(i + 1) % n]) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if j == i or j == (i + 1) % n or i == (j + 1) % n:
                continue
            if _segments_intersect(*edges[i], *edges[j]):
                return False, f"Edges {i} and {j} cross -- reconstruction is invalid"
    if len(set(ordered_points)) != n:
        return False, "Duplicate points in result"
    return True, "OK"


def sort_rectilinear_polygon(points):
    """Full pipeline: reconstruct boundary order, then validate it."""
    ordered = reconstruct_rectilinear_polygon(points)
    valid, message = validate_simple_polygon(ordered)
    if not valid:
        raise ValueError(f"Validation failed: {message}")
    return ordered


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
    return fig


if __name__ == "__main__":
    import random

    test_shapes = {
        "plus_shape": [(5, 2), (5, 3), (2, 3), (0, 3), (2, 2), (3, 5), (3, 2),
                        (2, 0), (0, 2), (3, 3), (2, 5), (3, 0)],
        "c_bracket_shape": [(0, 0), (6, 0), (6, 1), (1, 1), (1, 5), (6, 5), (6, 6), (0, 6)],
        "jdwk": [(5, 2), (5, 3), (2, 3), (0, 3), (2, 2), (3, 5), (3, 2), (2, 0), (0, 2), (3, 3), (2, 5), (3, 0)],
    }

    for name, pts in test_shapes.items():
        shuffled = pts[:]
        random.shuffle(shuffled)
        result = sort_rectilinear_polygon(pts)
        print(f"{name}: {result}")
        plot_sorted_polygon(result, title=name, save_path=f"{name}.png")