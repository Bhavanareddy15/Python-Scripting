"""
Entry point. Reads coordinate sets from an input file (default:
input/coordinates.txt; override with a command-line argument), one test
case per line, each line a Python-style list of (x, y) tuples. Sorts
each into boundary order (handling holes automatically), and saves a
labeled plot per test case to output/<input_filename>_output/testcase<N>.png
-- e.g. running against coordinates.txt saves into output/coordinates_output/.

Run from anywhere -- paths are anchored to this file's location, not
the current working directory.

Usage:
    python main.py                      # uses input/coordinates.txt
    python main.py my_shapes.txt        # uses input/my_shapes.txt
    python main.py /full/path/to.txt    # uses an absolute path as-is
"""

import os
import sys
import ast

from src.polygon_sort import sort_rectilinear_polygon_with_holes
from src.visualize import plot_sorted_polygon, plot_polygon_with_holes

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT_NAME = "coordinates.txt"


def resolve_input_path(arg):
    """A bare filename is looked up inside input/; a path containing a
    separator (or an absolute path) is used as given."""
    if arg is None:
        arg = DEFAULT_INPUT_NAME
    if os.path.isabs(arg) or os.sep in arg:
        return arg
    return os.path.join(SCRIPT_DIR, "input", arg)


def load_test_cases(path):
    """Each non-empty, non-comment line is parsed as a list of (x, y) tuples."""
    cases = []
    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                points = ast.literal_eval(line)
                points = [tuple(p) for p in points]
            except (ValueError, SyntaxError) as e:
                raise ValueError(f"Could not parse line {line_num}: {line!r}") from e
            cases.append(points)
    return cases


def main():
    input_path = resolve_input_path(sys.argv[1] if len(sys.argv) > 1 else None)
    input_basename = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.join(SCRIPT_DIR, "output", f"{input_basename}_output")

    if not os.path.isfile(input_path):
        print(f"Input file not found: {input_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    test_cases = load_test_cases(input_path)

    if not test_cases:
        print(f"No test cases found in {input_path}")
        return

    for i, points in enumerate(test_cases, start=1):
        name = f"testcase{i}"
        try:
            result = sort_rectilinear_polygon_with_holes(points)
            save_path = os.path.join(output_dir, f"{name}.png")
            if result['holes']:
                plot_polygon_with_holes(result, title=name, save_path=save_path)
                print(f"{name}: OK (outer + {len(result['holes'])} hole(s)) -> "
                      f"outer={result['outer']}, holes={result['holes']}")
            else:
                plot_sorted_polygon(result['outer'], title=name, save_path=save_path)
                print(f"{name}: OK -> {result['outer']}")
            print(f"    saved: {save_path}")
        except ValueError as e:
            print(f"{name}: FAILED -- {e}")


if __name__ == "__main__":
    main()