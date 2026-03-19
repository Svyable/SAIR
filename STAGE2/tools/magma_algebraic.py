from itertools import product

# Let me do a completely exhaustive search on size 4 for Problems 0 and 1.
# Size 4: 4^16 = 4,294,967,296 -- too many for full exhaustive.
# BUT: for Problem 1, we can prune early.
# P1: x = f(y, f(f(y, f(y,x)), x)) for all x,y in S
# For each partial table, we can check if P still could hold.

# Actually, let me be smarter. For Problem 1, P has only 2 free vars.
# On size n, that's n^2 constraints. Each constraint involves at most
# ~4 table lookups. So for size 4, 16 constraints.

# Let me try a backtracking approach for size 4.

SIZE = 4
S = list(range(SIZE))

# Table: f[a][b] for a,b in S
# We fill f[0][0], f[0][1], ..., f[0][3], f[1][0], ..., f[3][3]

def solve_p1():
    f = [[None]*SIZE for _ in range(SIZE)]

    def lookup(a, b):
        return f[a][b]

    def check_p1_constraint(x, y):
        """Check if x = f(y, f(f(y, f(y,x)), x)) with current partial table.
        Returns True if satisfied, False if violated, None if can't determine."""
        # Step 1: f(y,x)
        v1 = lookup(y, x)
        if v1 is None: return None

        # Step 2: f(y, v1)
        v2 = lookup(y, v1)
        if v2 is None: return None

        # Step 3: f(v2, x)
        v3 = lookup(v2, x)
        if v3 is None: return None

        # Step 4: f(y, v3)
        v4 = lookup(y, v3)
        if v4 is None: return None

        return x == v4

    def check_c1_constraint(x, y, z):
        """Check x = f(f(y, f(z,y)), f(y,x))"""
        v1 = lookup(z, y)
        if v1 is None: return None
        v2 = lookup(y, v1)
        if v2 is None: return None
        v3 = lookup(y, x)
        if v3 is None: return None
        v4 = lookup(v2, v3)
        if v4 is None: return None
        return x == v4

    solutions = []
    c_failures = []

    def backtrack(pos):
        if len(solutions) > 100 or len(c_failures) > 0:
            return

        if pos == SIZE * SIZE:
            # Full table, check all P constraints
            ok = True
            for x in S:
                for y in S:
                    r = check_p1_constraint(x, y)
                    if r is not True:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                table_copy = [row[:] for row in f]
                # Check C
                c_ok = True
                for x in S:
                    for y in S:
                        for z in S:
                            r = check_c1_constraint(x, y, z)
                            if r is not True:
                                c_ok = False
                                c_failures.append((table_copy, (x,y,z)))
                                return
                solutions.append(table_copy)
            return

        a = pos // SIZE
        b = pos % SIZE

        for v in S:
            f[a][b] = v

            # Check any P constraints that are now fully determined
            feasible = True
            for x in S:
                for y in S:
                    r = check_p1_constraint(x, y)
                    if r is False:
                        feasible = False
                        break
                if not feasible:
                    break

            if feasible:
                backtrack(pos + 1)

        f[a][b] = None

    print("Problem 1: Backtracking search on size 4...")
    backtrack(0)
    print(f"  Found {len(solutions)} solutions satisfying P")
    if c_failures:
        print(f"  COUNTEREXAMPLE FOUND!")
        table, cx = c_failures[0]
        for i in S:
            print(f"    f({i},*) = {table[i]}")
        print(f"    C fails at {cx}")
    else:
        print(f"  All solutions also satisfy C")
        for sol in solutions[:5]:
            print(f"  Solution:")
            for i in S:
                print(f"    f({i},*) = {sol[i]}")

solve_p1()

# Now Problem 0 on size 4 with backtracking
def solve_p0():
    f = [[None]*SIZE for _ in range(SIZE)]

    def lookup(a, b):
        return f[a][b]

    def check_p0_constraint(x, y, z, w):
        """Check f(x, f(y,z)) = f(f(y,w), w)"""
        v1 = lookup(y, z)
        if v1 is None: return None
        v2 = lookup(x, v1)
        if v2 is None: return None

        v3 = lookup(y, w)
        if v3 is None: return None
        v4 = lookup(v3, w)
        if v4 is None: return None

        return v2 == v4

    solutions = []
    c_failures = []

    def backtrack(pos):
        if len(solutions) > 100 or len(c_failures) > 0:
            return

        if pos == SIZE * SIZE:
            ok = True
            for x,y,z,w in product(S, repeat=4):
                r = check_p0_constraint(x,y,z,w)
                if r is not True:
                    ok = False
                    break
            if ok:
                table_copy = [row[:] for row in f]
                # Check C: x*(y*y) = (z*w)*u for all x,y,z,w,u
                c_ok = True
                for x,y,z,w,u in product(S, repeat=5):
                    lhs = lookup(x, lookup(y,y))
                    rhs = lookup(lookup(z,w), u)
                    if lhs != rhs:
                        c_ok = False
                        c_failures.append((table_copy, (x,y,z,w,u)))
                        return
                solutions.append(table_copy)
            return

        a = pos // SIZE
        b = pos % SIZE

        for v in S:
            f[a][b] = v

            feasible = True
            for x,y,z,w in product(S, repeat=4):
                r = check_p0_constraint(x,y,z,w)
                if r is False:
                    feasible = False
                    break

            if feasible:
                backtrack(pos + 1)

        f[a][b] = None

    print("\nProblem 0: Backtracking search on size 4...")
    backtrack(0)
    print(f"  Found {len(solutions)} solutions satisfying P")
    if c_failures:
        print(f"  COUNTEREXAMPLE FOUND!")
        table, cx = c_failures[0]
        for i in S:
            print(f"    f({i},*) = {table[i]}")
        print(f"    C fails at {cx}")
    else:
        print(f"  All solutions also satisfy C")
        for sol in solutions[:5]:
            print(f"  Solution:")
            for i in S:
                print(f"    f({i},*) = {sol[i]}")

solve_p0()
