from itertools import product
import random

# Let's first understand what P forces in each problem.

# Problem 0: P: x*(y*z) = (y*w)*w for all x,y,z,w
# Setting z=w: x*(y*z) = (y*z)*z for all x,y,z
# This means x*(y*z) depends only on y,z (not on x!) -- so f(x, t) is constant in x for t in range(f).
# Also (y*w)*w = x*(y*w) -- so f(t,w) = f(x,t) for t = y*w.
# Actually let's think more carefully.
# From P: f(x, f(y,z)) = f(f(y,w), w) for all x,y,z,w.
# The LHS depends on x, the RHS does not depend on x.
# So f(x, f(y,z)) is independent of x.
# That means: for any t in Im(f) (range of f), f(x,t) is constant in x.
# Let's call this constant g(t) for t in Im(f).
#
# Also from P with different w values:
# f(f(y,w1), w1) = f(f(y,w2), w2) for all y, w1, w2
# So f(f(y,w), w) is independent of w. Call it h(y).
# And h(y) = g(f(y,z)) for any z.
# So h(y) is also independent of z, which it is since g(f(y,z)) and f(y,z) might vary with z
# but g is applied... wait, g(f(y,z)) = f(x, f(y,z)) = h(y), so g(f(y,z)) is independent of z.
# This means g is constant on {f(y,z) : z in S} for each y.

# For the conclusion C: x*(y*y) = (z*w)*u for all x,y,z,w,u
# LHS: f(x, f(y,y)). Since f(y,y) is in Im(f), f(x, f(y,y)) = g(f(y,y)) = h(y).
# RHS: f(f(z,w), u). f(z,w) is in Im(f), so... wait, u is arbitrary, not just in Im(f).
# f(f(z,w), u) -- here f(z,w) is in Im(f), but we need f(t, u) for ALL u, not just f(x,t).
# We showed f(x, t) is const in x for t in Im(f). So f(t, u) for t in Im(f):
# wait, the first argument varies, second is fixed. That's different!
# f(x, t) const in x means: varying the FIRST arg doesn't matter when SECOND is in Im(f).
# But f(t, u) has t in Im(f) as FIRST arg, u as SECOND. This is f applied to (something in Im(f), u).
# We don't know that f(t, u) is constant in t or u.

# So C requires f(f(z,w), u) to be constant in z,w,u AND equal to h(y) for all y.
# f(f(z,w), u) must be constant = some value c, and h(y) = c for all y.
# h(y) = f(f(y,w),w) must be the same for all y.

# So the question is: can we have h not constant?
# h(y) = f(f(y,w), w) (for any w, same value).
# If we pick w and vary y, can f(f(y,w),w) change?

# Let's try to construct a counterexample.
# We need: h(y1) != h(y2) for some y1, y2
# AND: f(x,t) is constant in x for t in Im(f).
# AND: f(f(y,w),w) is independent of w.

# Let me try on {0,1,2,3} (4 elements) with random search.
def test_random(size, num_trials=500000):
    S = list(range(size))

    for trial in range(num_trials):
        # Random operation table
        table = {}
        for i in S:
            for j in S:
                table[(i,j)] = random.randint(0, size-1)

        def f(a,b):
            return table[(a,b)]

        # Check P: x*(y*z) = (y*w)*w
        p_holds = True
        for x,y,z,w in product(S, repeat=4):
            if f(x, f(y,z)) != f(f(y,w), w):
                p_holds = False
                break
        if not p_holds:
            continue

        # Check C: x*(y*y) = (z*w)*u
        c_holds = True
        cx = None
        for x,y,z,w,u in product(S, repeat=5):
            if f(x, f(y,y)) != f(f(z,w), u):
                c_holds = False
                cx = (x,y,z,w,u)
                break

        if not c_holds:
            print(f"COUNTEREXAMPLE for Problem 0 on size {size}!")
            print(f"  Table: {table}")
            for i in S:
                row = [f(i,j) for j in S]
                print(f"  f({i},*) = {row}")
            print(f"  C fails at {cx}")
            return True

    return False

print("Problem 0: random search on size 4...")
if not test_random(4, 200000):
    print("  No counterexample found in 200000 random trials on size 4")

print("\nProblem 0: random search on size 5...")
if not test_random(5, 200000):
    print("  No counterexample found in 200000 random trials on size 5")

# Problem 1 random search
def test_random_p1(size, num_trials=500000):
    S = list(range(size))

    for trial in range(num_trials):
        table = {}
        for i in S:
            for j in S:
                table[(i,j)] = random.randint(0, size-1)

        def f(a,b):
            return table[(a,b)]

        # Check P: x = y*((y*(y*x))*x)
        p_holds = True
        for x,y in product(S, repeat=2):
            if x != f(y, f(f(y, f(y, x)), x)):
                p_holds = False
                break
        if not p_holds:
            continue

        # Check C: x = (y*(z*y))*(y*x)
        c_holds = True
        cx = None
        for x,y,z in product(S, repeat=3):
            if x != f(f(y, f(z,y)), f(y,x)):
                c_holds = False
                cx = (x,y,z)
                break

        if not c_holds:
            print(f"COUNTEREXAMPLE for Problem 1 on size {size}!")
            for i in S:
                row = [f(i,j) for j in S]
                print(f"  f({i},*) = {row}")
            print(f"  C fails at {cx}")
            return True

    return False

print("\nProblem 1: random search on size 4...")
if not test_random_p1(4, 200000):
    print("  No counterexample found")

print("\nProblem 1: random search on size 5...")
if not test_random_p1(5, 200000):
    print("  No counterexample found")
