"""
Summary verification script: test all 4 problems on sizes 2-3 exhaustively,
plus Problem 1 on size 4 (feasible since P has only 2 vars).
"""
from itertools import product

def F(t, a, b):
    return t[(a,b)]

def test_all(name, p_fn, c_fn, p_nv, c_nv, sizes):
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}")
    for size in sizes:
        S = list(range(size))
        count_p = 0
        count_cx = 0
        first_cx = None
        for tup in product(S, repeat=size*size):
            table = {}
            idx = 0
            for i in S:
                for j in S:
                    table[(i,j)] = tup[idx]; idx += 1

            p_ok = all(p_fn(table, S, v) for v in product(S, repeat=p_nv))
            if not p_ok: continue
            count_p += 1

            c_ok = all(c_fn(table, S, v) for v in product(S, repeat=c_nv))
            if not c_ok:
                count_cx += 1
                if first_cx is None:
                    first_cx = [table[(i,j)] for i in S for j in S]

        status = "ALL satisfy C" if count_cx == 0 else f"{count_cx} COUNTEREXAMPLES"
        print(f"  Size {size}: {count_p} models of P, {status}")
        if first_cx:
            print(f"    First counterexample op: {first_cx}")

# Problem 0
def p0P(t,S,v): x,y,z,w=v; return F(t,x,F(t,y,z))==F(t,F(t,y,w),w)
def p0C(t,S,v): x,y,z,w,u=v; return F(t,x,F(t,y,y))==F(t,F(t,z,w),u)
test_all("Problem 0 (claimed FALSE): x*(y*z)=(y*w)*w => x*(y*y)=(z*w)*u", p0P, p0C, 4, 5, [2,3])

# Problem 1
def p1P(t,S,v): x,y=v; return x==F(t,y,F(t,F(t,y,F(t,y,x)),x))
def p1C(t,S,v): x,y,z=v; return x==F(t,F(t,y,F(t,z,y)),F(t,y,x))
test_all("Problem 1 (claimed FALSE): x=y*((y*(y*x))*x) => x=(y*(z*y))*(y*x)", p1P, p1C, 2, 3, [2,3,4])

# Problem 2
def p2P(t,S,v): x,y,z=v; return F(t,x,y)==F(t,y,F(t,x,F(t,z,x)))
def p2C(t,S,v): x,y,z=v; return F(t,x,y)==F(t,F(t,y,F(t,z,x)),y)
test_all("Problem 2 (claimed TRUE): x*y=y*(x*(z*x)) => x*y=(y*(z*x))*y", p2P, p2C, 3, 3, [2,3])

# Problem 3
def p3P(t,S,v): x,y,z=v; return x==F(t,F(t,F(t,F(t,y,y),x),x),z)
def p3C(t,S,v): x,y,z,w=v; return x==F(t,y,F(t,F(t,x,F(t,y,z)),w))
test_all("Problem 3 (claimed TRUE): x=(((y*y)*x)*x)*z => x=y*((x*(y*z))*w)", p3P, p3C, 3, 4, [2,3])

# Now let's print structural info about models
print("\n" + "="*70)
print("  STRUCTURAL ANALYSIS OF MODELS")
print("="*70)

# Problem 0 size 3: show all models
print("\nProblem 0, size 3 models:")
S = [0,1,2]
for tup in product(S, repeat=9):
    table = {}
    idx = 0
    for i in S:
        for j in S:
            table[(i,j)] = tup[idx]; idx += 1
    if all(p0P(table,S,v) for v in product(S,repeat=4)):
        im = set(table.values())
        rows = [[table[(i,j)] for j in S] for i in S]
        print(f"  rows={rows}, Im(f)={im}")

# Problem 1 size 4: show all models
print("\nProblem 1, size 4 models:")
S = [0,1,2,3]
count = 0
for tup in product(S, repeat=16):
    table = {}
    idx = 0
    for i in S:
        for j in S:
            table[(i,j)] = tup[idx]; idx += 1
    if all(p1P(table,S,v) for v in product(S,repeat=2)):
        rows = [[table[(i,j)] for j in S] for i in S]
        all_same = all(rows[i] == rows[0] for i in range(4))
        is_invol = all(rows[0][rows[0][x]] == x for x in S)
        print(f"  rows_identical={all_same}, involution={is_invol}, row0={rows[0]}")
        count += 1
print(f"  Total: {count} models")

# Problem 3: verify 0 models on sizes 2-4
print("\nProblem 3 model counts:")
for size in [2,3]:
    S = list(range(size))
    count = 0
    for tup in product(S, repeat=size*size):
        table = {}; idx = 0
        for i in S:
            for j in S:
                table[(i,j)] = tup[idx]; idx += 1
        if all(p3P(table,S,v) for v in product(S,repeat=3)):
            count += 1
    print(f"  Size {size}: {count} models of P")
