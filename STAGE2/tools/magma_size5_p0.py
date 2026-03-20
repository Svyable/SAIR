"""
Size 5 exhaustive for Problem 0 using constraint propagation.

P: f(x, f(y,z)) = f(f(y,w), w) for all x,y,z,w

Key structural constraints from P:
1. f(x,t) is constant in x for t in Im(f) => "column t" is constant for t in Im(f)
2. f(f(y,w),w) is independent of w => h(y) well-defined
3. g(f(y,z)) = h(y) for all y,z

Strategy: build the table using these constraints.
- First, determine Im(f) (it must be a subset of S).
- For t in Im(f), column t is constant: f(x,t) = g(t).
- h(y) = g(f(y,z)) must be independent of z.
- h(y) = f(f(y,w),w) must be independent of w.
"""

from itertools import product

SIZE = 5
S = list(range(SIZE))

# For P to hold, we need:
# 1. For each t in Im(f), f(x,t) is the same for all x.
# 2. For each y, g(f(y,z)) is the same for all z.
# 3. h(y) = f(f(y,w), w) for any w.

# Let's enumerate by choosing:
# - Which subset I ⊂ S is Im(f)
# - For t in I: g(t) = constant value of column t (g(t) must be in S, and for C we need g(t) to be specific)
# - For t not in I: column t can be anything (since no element maps to t)
# - The table f(a,b) for all a,b, subject to Im(f) = I and column constraints.

# Actually, let me just do a smarter backtracking.

count_p = 0
count_c_fail = 0

# We'll build f row by row. After each row is complete, check constraints.
f = [[None]*SIZE for _ in range(SIZE)]

def check_partial():
    """Check all verifiable P constraints with current partial table."""
    for x in S:
        for y in S:
            for z in S:
                yz = f[y][z]
                if yz is None: continue
                x_yz = f[x][yz]
                if x_yz is None: continue
                for w in S:
                    yw = f[y][w]
                    if yw is None: continue
                    yw_w = f[yw][w]
                    if yw_w is None: continue
                    if x_yz != yw_w:
                        return False
    return True

def check_column_constraint():
    """For any t that appears as a value, check f(x,t) is same for all filled x."""
    im = set()
    for i in S:
        for j in S:
            if f[i][j] is not None:
                im.add(f[i][j])

    for t in im:
        vals = set()
        for x in S:
            if f[x][t] is not None:
                vals.add(f[x][t])
        if len(vals) > 1:
            return False
    return True

solutions = []

def solve(pos):
    if count_c_fail > 0:
        return

    if pos == SIZE * SIZE:
        # Full table -- verify P
        for x,y,z,w in product(S, repeat=4):
            if f[x][f[y][z]] != f[f[y][w]][w]:
                return
        sol = [row[:] for row in f]
        solutions.append(sol)
        return

    row, col = pos // SIZE, pos % SIZE

    for v in S:
        f[row][col] = v

        # Quick constraint check: column constraint
        # Check if any column has inconsistent values
        ok = check_column_constraint()
        if not ok:
            f[row][col] = None
            continue

        # Check partial P constraints
        if not check_partial():
            f[row][col] = None
            continue

        solve(pos + 1)

    f[row][col] = None

print(f"Searching size {SIZE} for Problem 0...")
import time
t0 = time.time()
solve(0)
t1 = time.time()
print(f"Found {len(solutions)} models in {t1-t0:.1f}s")

for sol in solutions:
    print("  Model:")
    for i in S:
        print(f"    f({i},*) = {sol[i]}")

    # Check C
    ok = True
    for x,y,z,w,u in product(S, repeat=5):
        if sol[x][sol[y][y]] != sol[sol[z][w]][u]:
            ok = False
            print(f"    C FAILS at x={x},y={y},z={z},w={w},u={u}")
            break
    if ok:
        print(f"    C holds")
