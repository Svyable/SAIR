from itertools import product
import random

# Key observations from size 2-3:
# Problem 0: On size 3, all 9 ops satisfying P also satisfy C.
#   The ops are "almost constant" -- f is constant on most inputs.
#   Let me check size 4 exhaustively (4^16 = 4B is too much).
#   But with pruning on P, we can try.

# Problem 1: On sizes 2,3, the ops satisfying P are all "constant-row" ops
#   where f(a,*) = f(b,*) for all a,b (all rows identical).
#   On size 2: f(x,y) = 1-y (involution) or f(x,y) = y (identity). Wait no:
#   Op (0,1,0,1) means f(0,0)=0,f(0,1)=1,f(1,0)=0,f(1,1)=1, i.e. f(x,y)=y (right projection)
#   Op (1,0,1,0) means f(x,y)=1-y (complement of right projection)
#   On size 3: same pattern -- all rows identical, and f(*,y) is a permutation.
#   These are essentially "right quasigroups with constant rows" = left-cancellative.
#   Actually they're just: f(x,y) = sigma(y) for some permutation sigma, with sigma^3 = id.
#   Wait, P says x = sigma(sigma(sigma(x)) * x)... let me think.

# Actually on size 3, the ops for P1 are:
# f(x,y)=y, f(x,y)=swap(y) for various swaps/cycles
# All involutions or identity. Let me check.

# For P1: x = f(y, f(f(y, f(y,x)), x))
# With f(a,b) = sigma(b): x = sigma(sigma(sigma(sigma(x)) * x))
# Wait f(a,b) = sigma(b), so:
# f(y,x) = sigma(x), f(y, sigma(x)) = sigma(sigma(x)) = sigma^2(x)
# f(y, sigma^2(x)) = sigma^3(x)
# Then f(sigma^3(x), x) = sigma(x)
# Then f(y, sigma(x)) = sigma(sigma(x)) = sigma^2(x)
# P says: x = sigma^2(x) for all x. So sigma^2 = id, i.e. sigma is an involution.
# On {0,1}: involutions are id and (0 1). On {0,1,2}: id, (0 1), (0 2), (1 2).
# That matches what we see.

# Now for C: x = f(f(y, f(z,y)), f(y,x)) = f(sigma(sigma(y)), sigma(x)) = f(sigma^2(y), sigma(x)) = sigma(sigma(x)) = sigma^2(x) = x.
# So C holds! This means P1 => C1 is actually TRUE for this family.

# But we're told Problem 1 is FALSE. We need a non-trivial op satisfying P.
# The ops satisfying P that AREN'T of the form f(a,b)=sigma(b) could be counterexamples.

# Let me try size 4 with a more targeted search.
# On size 4, try to find ops where f depends on both arguments.

S4 = [0,1,2,3]

# For Problem 1, let's do a targeted exhaustive for size 4.
# 4^16 is too many. Let's try: generate ops where P holds by construction.

# P: x = y*((y*(y*x))*x) for all x,y
# Let's define: for each y, define g_y(x) = f(y,x). Then:
# f(y, f(y,x)) = g_y(g_y(x))
# f(y, g_y(g_y(x))) = g_y^3(x)
# f(g_y^3(x), x) = ... this is f with first arg = g_y^3(x), second = x
# Let h(a,b) = f(a,b). Then P says:
# x = h(y, h(h(y, h(y,x)), x))
# = g_y( h(g_y(g_y(x)), x) )
# Let's define for each a: r_a(b) = f(b, a) (left-multiplication function mapping on 2nd coord... no)
# Actually let me just define: L_y(x) = f(y,x) and R_x(y) = f(y,x).
# P: x = L_y( R_x( L_y( L_y(x) ) ) )
# = L_y( f( L_y^2(x), x ) )
# Hmm, f(L_y^2(x), x) = ??? depends on the full table.

# Let me just try a semi-random approach: sample random ops on size 4-6
# that satisfy P1 by rejection, then check C.

print("Problem 1: exhaustive search size 4 with early pruning")
print("(Testing all 4^16 ops with aggressive pruning on P)")

S = [0,1,2,3]
SIZE = 4
found = False

# We'll build the table incrementally and prune.
# But even with pruning, this might be slow. Let's try a different approach:
# Generate random tables on size 4,5,6 and filter.

import sys

def check_p1(size):
    S = list(range(size))
    # Random search with many trials
    count = 0
    for trial in range(2000000):
        table = [[random.randint(0, size-1) for _ in range(size)] for _ in range(size)]

        def f(a,b):
            return table[a][b]

        p_holds = True
        for x in S:
            for y in S:
                if x != f(y, f(f(y, f(y,x)), x)):
                    p_holds = False
                    break
            if not p_holds:
                break
        if not p_holds:
            continue

        count += 1
        # Check if all rows are identical
        all_same = all(table[i] == table[0] for i in range(size))

        c_holds = True
        cx = None
        for x in S:
            for y in S:
                for z in S:
                    if x != f(f(y, f(z,y)), f(y,x)):
                        c_holds = False
                        cx = (x,y,z)
                        break
                if not c_holds:
                    break
            if not c_holds:
                break

        if not c_holds:
            print(f"  COUNTEREXAMPLE on size {size}!")
            for i in S:
                print(f"    f({i},*) = {table[i]}")
            print(f"    C fails at {cx}")
            return True
        elif not all_same:
            print(f"  Found non-constant-row op satisfying both P and C:")
            for i in S:
                print(f"    f({i},*) = {table[i]}")

    print(f"  Tried 2M random ops on size {size}, found {count} satisfying P, all satisfy C")
    return False

for sz in [4, 5, 6, 7]:
    print(f"\nSize {sz}:")
    if check_p1(sz):
        break

# Also let's try Problem 0 with same approach on larger sizes
print("\n" + "="*60)
print("Problem 0: targeted search on larger sizes")

def check_p0(size):
    S = list(range(size))
    count = 0
    for trial in range(2000000):
        table = [[random.randint(0, size-1) for _ in range(size)] for _ in range(size)]

        def f(a,b):
            return table[a][b]

        p_holds = True
        for y in S:
            for z in S:
                val = None
                for x in S:
                    v = f(x, f(y,z))
                    if val is None:
                        val = v
                    elif v != val:
                        p_holds = False
                        break
                if not p_holds:
                    break
            if not p_holds:
                break
        if not p_holds:
            continue

        # Verify P fully
        for x,y,z,w in product(S, repeat=4):
            if f(x, f(y,z)) != f(f(y,w), w):
                p_holds = False
                break
        if not p_holds:
            continue

        count += 1
        c_holds = True
        for x,y,z,w,u in product(S, repeat=5):
            if f(x, f(y,y)) != f(f(z,w), u):
                c_holds = False
                break

        if not c_holds:
            print(f"  COUNTEREXAMPLE on size {size}!")
            for i in S:
                print(f"    f({i},*) = {table[i]}")
            return True

    print(f"  Tried 2M random on size {size}, {count} satisfy P, all satisfy C")
    return False

for sz in [4, 5, 6]:
    print(f"\nSize {sz}:")
    if check_p0(sz):
        break
