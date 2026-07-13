"""
Core algorithm for reconstructing the boundary order of a simple,
axis-aligned (rectilinear) polygon from an unordered point set.
"""

from collections import defaultdict


def reconstruct_rectilinear_polygon(points):
    """
    Reconstruct boundary order via the even-odd parity rule: group points
    sharing an x (or y) coordinate, sort by the other coordinate, and pair
    them up (1st-2nd, 3rd-4th, ...) as real boundary edges. A line through
    a simple polygon crosses its boundary an even number of times,
    alternating inside/outside -- this holds for ANY simple orthogonal
    polygon, star-shaped or not.

    Starts at the leftmost point (ties broken by smallest y), walks the
    boundary, and returns it in counter-clockwise order.
    """
    if len(points) < 4:
        raise ValueError("Need at least 4 points for a rectilinear polygon")

    by_x = defaultdict(list)
    by_y = defaultdict(list)
    for p in points:
        by_x[p[0]].append(p)
        by_y[p[1]].append(p)

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

    if _signed_area(ordered) < 0:
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
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return _collinear_overlap(p1, p2, p3, p4)


def _collinear_overlap(a, b, c, d):
    if a[0] == b[0] == c[0] == d[0]:
        lo1, hi1 = sorted([a[1], b[1]])
        lo2, hi2 = sorted([c[1], d[1]])
        return max(lo1, lo2) < min(hi1, hi2)
    if a[1] == b[1] == c[1] == d[1]:
        lo1, hi1 = sorted([a[0], b[0]])
        lo2, hi2 = sorted([c[0], d[0]])
        return max(lo1, lo2) < min(hi1, hi2)
    return False


def validate_simple_polygon(ordered_points):
    """Confirms no two non-adjacent edges cross (including collinear
    overlaps). Returns (is_valid: bool, message: str)."""
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
