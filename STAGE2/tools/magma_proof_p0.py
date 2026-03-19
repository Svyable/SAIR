"""
Algebraic proof attempt for Problem 0: P: x*(y*z) = (y*w)*w => C: x*(y*y) = (z*w)*u

Key derivations from P:

1. From P: f(x, f(y,z)) = f(f(y,w), w) -- RHS independent of x
   => f(x, t) is constant in x for every t in Im(f).
   Notation: for t in Im(f), define g(t) = f(x,t) (any x).

2. From P: f(f(y,w), w) doesn't depend on z either.
   And f(f(y,w1), w1) = f(f(y,w2), w2) for all w1, w2.
   Define h(y) = f(f(y,w), w) for any w.
   So P says: f(x, f(y,z)) = h(y).

3. For the LHS of C: f(x, f(y,y)). Since f(y,y) in Im(f):
   f(x, f(y,y)) = g(f(y,y)) = h(y) [from step 2 with z=y].

4. For the RHS of C: f(f(z,w), u).
   Need to show this equals h(y) for all y,z,w,u.
   Equivalently, f(f(z,w), u) must be constant.

5. Key step: from P, set y=z, z=w to get:
   f(x, f(z,w)) = h(z) = f(f(z,v), v) for any v.
   So g(f(z,w)) = h(z).

6. Now consider f(s, u) where s = f(z,w) in Im(f).
   From step 5: g(s) = h(z) whenever s = f(z,w).
   From step 1: g(s) = f(a, s) for any a. In particular g(s) = f(s, s).

7. From P: f(x, f(y,z)) = f(f(y,w), w).
   Set x = f(y,w), z arbitrary:
   f(f(y,w), f(y,z)) = f(f(y,w'), w').
   LHS: f(f(y,w), f(y,z)). f(y,z) is in Im(f), so f(f(y,w), f(y,z)) = g(f(y,z)) = h(y).
   RHS: h(y). Consistent, no new info.

8. Can we derive f(s, u) for s in Im(f) and ARBITRARY u?
   From P set y = s for some s:
   f(x, f(s,z)) = h(s).
   This means g(f(s,z)) = h(s), i.e., f(s,-) maps everything into the set
   {t : g(t) = h(s)}.

9. From P, h(y) = f(f(y,w), w). Set w = u:
   h(y) = f(f(y,u), u).
   So for ANY a,u: f(a, u) = ??? We know f(f(y,u), u) = h(y).
   So if a = f(y,u) for some y, then f(a,u) = h(y).

   But WHAT IF a is NOT in Im(f(-, u)) = {f(y,u) : y in S}?
   Then we have no constraint on f(a,u) from this equation alone.

   However, the RHS of C is f(f(z,w), u). Here f(z,w) IS in Im(f),
   and specifically in Im(f(z,-)). But is it in Im(f(-,u))?
   Not necessarily in general.

10. NEW APPROACH: Let's show f(s, u) = g(s) for s in Im(f).
    Wait, that's backwards. g(t) = f(x,t) = constant in x.
    We need f(s, u) -- s is first arg, u is second.
    These are different positions.

    Actually, is there a way to show Im(f) is a "left zero" or similar?

11. Consider: from step 8, f(s,z) maps into {t : g(t) = h(s)} for all z.
    In particular f(s, f(s,z)) = g(f(s,z)) [since f(s,z) in Im(f)] = h(s).
    Also f(s, u) for arbitrary u: from P with y=s, we get
    f(x, f(s, u)) = h(s) for all x, i.e., g(f(s,u)) = h(s).

    So f(s,-) maps S into {t : g(t) = h(s)}.
    And f(s,z) is always in Im(f) (since f(s,z) is a value of f).
    So f(s,z) in Im(f) and g(f(s,z)) = h(s).

12. Now for C's RHS: f(f(z,w), u).
    s = f(z,w) in Im(f). From step 11, f(s, u) is in Im(f) and
    g(f(s,u)) = h(s).

    But we need f(s,u) itself, not g(f(s,u)).

13. KEY INSIGHT: From P, f(x, f(y,z)) = h(y) for all x,y,z.
    Set y = f(z,w) (which is allowed, y is universally quantified):
    f(x, f(f(z,w), u)) = h(f(z,w)) for all x, z, w, u.

    So g(f(f(z,w), u)) = h(f(z,w)).

    And what is h(f(z,w))? From step 5: h(y) = g(f(y, anything)).
    h(f(z,w)) = g(f(f(z,w), anything)).
    From step 13 above: g(f(f(z,w), u)) = h(f(z,w)).
    This is consistent but circular.

    But from step 2: h(y) = f(x, f(y, z)) for any x,z.
    h(f(z,w)) = f(x, f(f(z,w), anything)).

    Also from step 2: f(x, f(y,z)) = h(y).
    So f(x, f(f(z,w), u)) = h(f(z,w)) = f(x', f(f(z,w), u')) for any x', u'.
    This says f(f(z,w), u) is in Im(f) and g maps it to h(f(z,w)).

14. We need f(f(z,w), u) = h(y) for all y,z,w,u. i.e., it's constant.
    We've shown g(f(f(z,w), u)) = h(f(z,w)). If we can show h is constant, done!
    Because then g(f(f(z,w),u)) = const, and f(f(z,w),u) might vary but...
    Actually we need f(f(z,w),u) itself to be constant, not just g of it.

15. So the question reduces to: does P force h to be constant?
    h(y) = f(x, f(y,z)) for any x,z.
    h(y1) vs h(y2): if f(y1, z) = f(y2, z') for some z, z', then... no.

    Actually on our size-3 examples, h was always constant. Let me verify
    if h is always constant by checking size 4 models.
"""

from itertools import product

print("Checking if h(y) = f(f(y,w),w) is constant in all size-4 models of P0:")
S4 = [0,1,2,3]

# Use backtracking for size 4
SIZE = 4
f_table = [[None]*SIZE for _ in range(SIZE)]

def F(a,b):
    return f_table[a][b]

def check_p0(x,y,z,w):
    v1 = f_table[y][z] if f_table[y] and f_table[y][z] is not None else None
    if v1 is None: return None
    v2 = f_table[x][v1] if f_table[x] and f_table[x][v1] is not None else None
    if v2 is None: return None
    v3 = f_table[y][w] if f_table[y] and f_table[y][w] is not None else None
    if v3 is None: return None
    v4 = f_table[v3][w] if f_table[v3] and f_table[v3][w] is not None else None
    if v4 is None: return None
    return v2 == v4

solutions = []

def backtrack(pos):
    if len(solutions) >= 200:
        return
    if pos == SIZE * SIZE:
        # Verify fully
        for x,y,z,w in product(S4, repeat=4):
            if f_table[x][f_table[y][z]] != f_table[f_table[y][w]][w]:
                return
        sol = [row[:] for row in f_table]
        solutions.append(sol)
        return

    a, b = pos // SIZE, pos % SIZE
    for v in S4:
        f_table[a][b] = v
        feasible = True
        for x,y,z,w in product(S4, repeat=4):
            vals = [f_table[y][z] if f_table[y][z] is not None else -1,
                    f_table[y][w] if f_table[y][w] is not None else -1]
            if vals[0] == -1 or vals[1] == -1:
                continue
            lhs_inner = f_table[x][vals[0]] if f_table[x][vals[0]] is not None else -1
            rhs_inner = f_table[vals[1]][w] if f_table[vals[1]][w] is not None else -1
            if lhs_inner == -1 or rhs_inner == -1:
                continue
            if lhs_inner != rhs_inner:
                feasible = False
                break
        if feasible:
            backtrack(pos + 1)
    f_table[a][b] = None

backtrack(0)
print(f"Found {len(solutions)} models of P on size 4")

h_constant_count = 0
h_nonconstant = []
for sol in solutions:
    # h(y) = f(f(y,0), 0) for w=0 (should be same for all w)
    h_vals = set()
    for y in S4:
        h_y = sol[sol[y][0]][0]  # h(y) = f(f(y,w), w) with w=0
        h_vals.add(h_y)
    if len(h_vals) == 1:
        h_constant_count += 1
    else:
        h_nonconstant.append((sol, h_vals))

print(f"h constant: {h_constant_count}, h non-constant: {len(h_nonconstant)}")
if h_nonconstant:
    sol, hv = h_nonconstant[0]
    print(f"  Example: h values = {hv}")
    for i in S4:
        print(f"    f({i},*) = {sol[i]}")

# Check C on all solutions
c_fail = 0
for sol in solutions:
    ok = True
    for x,y,z,w,u in product(S4, repeat=5):
        if sol[x][sol[y][y]] != sol[sol[z][w]][u]:
            ok = False
            break
    if not ok:
        c_fail += 1
        print(f"  C FAILS on:")
        for i in S4:
            print(f"    f({i},*) = {sol[i]}")
        break

if c_fail == 0:
    print("All solutions satisfy C")
