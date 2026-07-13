# Rectilinear Polygon Sorter

Takes an unordered list of (x, y) coordinates for a simple, axis-aligned
(rectilinear) polygon and reconstructs the boundary in counter-clockwise
order, starting from the leftmost point (ties broken by smallest y).

## Project structure

```
rectilinear_polygon_sorter/
├── main.py                 # entry point -- run this
├── input/
│   └── coordinates.txt     # one test case per line
├── output/                 # generated images land here (testcase1.png, ...)
├── src/
│   ├── __init__.py
│   ├── polygon_sort.py     # core algorithm + validation (no I/O)
│   └── visualize.py        # plotting only
└── README.md
```

## Usage

1. Edit `input/coordinates.txt`. Each line is one test case: a Python-style
   list of (x, y) tuples, e.g.

   ```
   [(0, 0), (4, 0), (4, 4), (0, 4)]
   [(0,0),(2,0),(2,2),(4,2),(4,0),(6,0),(6,6),(4,6),(4,4),(2,4),(2,6),(0,6)]
   ```

   Lines starting with `#` and blank lines are ignored.

2. Run:
   ```
   python main.py
   ```
   (Works from any working directory -- paths are anchored to the
   script's own location, not wherever you happened to launch it from.)

3. Check `output/`. Each line produces `testcase1.png`, `testcase2.png`, etc.,
   and the sorted coordinate list is printed to the console.

## Notes

- Assumes the polygon is simple (no self-intersections) and rectilinear
  (every edge horizontal or vertical). Non-rectilinear input will raise
  an error rather than silently producing a wrong answer.
- `polygon_sort.py` has no plotting or file I/O in it -- it's pure logic,
  so it can be imported and unit-tested independently of `visualize.py`.
