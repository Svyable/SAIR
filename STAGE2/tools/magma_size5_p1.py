"""
Size 5 search for Problem 1.
P: x = y*((y*(y*x))*x)  C: x = (y*(z*y))*(y*x)
"""
from itertools import product
import time

SIZE = 5
S = list(range(SIZE))

f = [[None]*SIZE for _ in range(SIZE)]
count_c_fail = 0
counterexamples = []

def check_partial_p1():
    """Check P: x = f(y, f(f(y, f(y,x)), x)) for all filled entries."""
    for x in S:
        for y in S:
            v1 = f[y][x]
            if v1 is None: continue
            v2 = f[y][v1]
            if v2 is None: continue
            v3 = f[v2][x]
            if v3 is None: continue
            v4 = f[y][v3]
            if v4 is None: continue
            if x != v4:
                return False
    return True

def solve(pos):
    global count_c_fail
    if count_c_fail > 0:
        return

    if pos == SIZE * SIZE:
        # Verify P fully
        for x in S:
            for y in S:
                v1 = f[y][x]
                v2 = f[y][v1]
                v3 = f[v2][x]
                v4 = f[y][v3]
                if x != v4:
                    return

        sol = [row[:] for row in f]

        # Check C: x = f(f(y, f(z,y)), f(y,x))
        for x in S:
            for y in S:
                for z in S:
                    v1 = f[z][y]
                    v2 = f[y][v1]
                    v3 = f[y][x]
                    v4 = f[v2][v3]
                    if x != v4:
                        count_c_fail += 1
                        counterexamples.append((sol, (x,y,z)))
                        return

        # All rows same?
        all_same = all(f[i] == f[0] for i in range(SIZE))
        if not all_same:
            print(f"  Non-identical-row model found!")
            for i in S:
                print(f"    f({i},*) = {f[i]}")
        return

    row, col = pos // SIZE, pos % SIZE

    for v in S:
        f[row][col] = v
        if check_partial_p1():
            solve(pos + 1)
        if count_c_fail > 0:
            f[row][col] = None
            return

    f[row][col] = None

print(f"Searching size {SIZE} for Problem 1...")
t0 = time.time()
solve(0)
t1 = time.time()
print(f"Search took {t1-t0:.1f}s")

if counterexamples:
    sol, cx = counterexamples[0]
    print(f"COUNTEREXAMPLE FOUND!")
    for i in S:
        print(f"  f({i},*) = {sol[i]}")
    print(f"  C fails at x={cx[0]},y={cx[1]},z={cx[2]}")

    # Verify
    def F(a,b): return sol[a][b]
    ok = True
    for x in S:
        for y in S:
            if x != F(y, F(F(y, F(y,x)), x)):
                print(f"  P FAILS - BUG!")
                ok = False
                break
        if not ok: break
    if ok:
        print(f"  P verified OK")
else:
    print(f"No counterexample found on size {SIZE}")
