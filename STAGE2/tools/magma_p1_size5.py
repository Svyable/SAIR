from itertools import product

# Problem 1 on size 4: all 10 solutions are involutions applied uniformly
# (f(a,b) = sigma(b) where sigma^2 = id)
# On size 4 there are exactly 10 involutions on {0,1,2,3}:
# id, (01), (02), (03), (12), (13), (23), (01)(23), (02)(13), (03)(12)
# That's 10. Perfect match!

# Proof that P1 forces f(a,b) = sigma(b) with sigma^2 = id:
# P: x = f(y, f(f(y, f(y,x)), x)) for all x,y
#
# Claim: for these ops, C holds.
# C: x = f(f(y, f(z,y)), f(y,x))
# = f(f(y, sigma(y)), sigma(x))
# Now f(y, sigma(y)) = sigma(sigma(y)) = y (since sigma^2 = id)
# So = f(y, sigma(x)) = sigma(sigma(x)) = x. QED.
#
# But wait - we need to show P FORCES f(a,b) = sigma(b).
# Let's verify: does P force all rows to be identical?

# P with y=y0 fixed: x = f(y0, f(f(y0, f(y0,x)), x))
# Define g = f(y0, -). Then: x = g(f(g(g(x)), x))
# This must hold for all x.
# If all rows are NOT identical, can P still hold?

# From size 4 exhaustive: all 10 solutions have identical rows.
# This strongly suggests P forces f(a,b) to be independent of a.

# Let me prove it. Set y=a and y=b in P:
# x = f(a, f(f(a, f(a,x)), x))
# x = f(b, f(f(b, f(b,x)), x))
# So f(a, f(f(a, f(a,x)), x)) = f(b, f(f(b, f(b,x)), x))
# This doesn't immediately show rows are equal.

# But let's try: in P, set x = f(y,t) for some t:
# f(y,t) = f(y, f(f(y, f(y, f(y,t))), f(y,t)))
# Hmm, complex.

# Let me try to find a non-involution counterexample on larger sizes.
# On size 5: involutions on {0,...,4}: id + C(5,2) + C(5,2)*C(3,2)/2!/...
# = 1 + 10 + 15 = 26 involutions.

# Let me just try size 5 backtracking for Problem 1.

SIZE = 5
S = list(range(SIZE))

f_table = [[None]*SIZE for _ in range(SIZE)]

def lookup(a, b):
    return f_table[a][b]

def check_p1(x, y):
    v1 = lookup(y, x)
    if v1 is None: return None
    v2 = lookup(y, v1)
    if v2 is None: return None
    v3 = lookup(v2, x)
    if v3 is None: return None
    v4 = lookup(y, v3)
    if v4 is None: return None
    return x == v4

solutions = []
c_failures = []

def backtrack(pos):
    if len(solutions) >= 30 or len(c_failures) > 0:
        return

    if pos == SIZE * SIZE:
        ok = True
        for x in S:
            for y in S:
                r = check_p1(x, y)
                if r is not True:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            table_copy = [row[:] for row in f_table]
            # Check C
            for x in S:
                for y in S:
                    for z in S:
                        v1 = lookup(z, y)
                        v2 = lookup(y, v1)
                        v3 = lookup(y, x)
                        v4 = lookup(v2, v3)
                        if x != v4:
                            c_failures.append((table_copy, (x,y,z)))
                            return
            solutions.append(table_copy)
        return

    a = pos // SIZE
    b = pos % SIZE

    for v in S:
        f_table[a][b] = v

        feasible = True
        for x in S:
            for y in S:
                r = check_p1(x, y)
                if r is False:
                    feasible = False
                    break
            if not feasible:
                break

        if feasible:
            backtrack(pos + 1)

    f_table[a][b] = None

print("Problem 1: Backtracking on size 5...")
backtrack(0)
print(f"  Found {len(solutions)} solutions, {len(c_failures)} counterexamples")
if c_failures:
    table, cx = c_failures[0]
    for i in S:
        print(f"    f({i},*) = {table[i]}")
    print(f"    C fails at {cx}")
else:
    # Check: are they all involution-type?
    for sol in solutions:
        row0 = sol[0]
        all_same = all(sol[i] == row0 for i in range(SIZE))
        is_invol = all(row0[row0[x]] == x for x in S)
        print(f"  rows_same={all_same}, involution={is_invol}: row0={row0}")
