from itertools import product

# Exhaustive search on 4 elements for Problem 1
# P: x = y*((y*(y*x))*x) -- only 2 vars, so 16 checks per op
# C: x = (y*(z*y))*(y*x) -- 3 vars, so 64 checks per op
# 4^16 = 4294967296 ops -- too many for exhaustive

# But for Problem 1, P is very restrictive. Let's try size 3 exhaustive
# (already done above, found 4 ops all satisfying C)

# Let's try size 4 exhaustive for Problem 1 using pruning
# Actually 4^16 is 4 billion, way too many.

# Let me instead do exhaustive on size 3 for Problem 0 (already done, 9 ops)
# and enumerate them to understand the structure.

print("="*60)
print("Problem 0: Exhaustive on size 3, listing all ops satisfying P")
print("="*60)

S = [0,1,2]
SIZE = 3
count = 0
for t in product(S, repeat=SIZE*SIZE):
    table = {}
    for i in S:
        for j in S:
            table[(i,j)] = t[i*SIZE+j]

    def f(a,b):
        return table[(a,b)]

    p_holds = True
    for x,y,z,w in product(S, repeat=4):
        if f(x, f(y,z)) != f(f(y,w), w):
            p_holds = False
            break
    if not p_holds:
        continue

    count += 1
    print(f"\nOp #{count}:")
    for i in S:
        row = [f(i,j) for j in S]
        print(f"  f({i},*) = {row}")

    # Check C
    c_holds = True
    for x,y,z,w,u in product(S, repeat=5):
        if f(x, f(y,y)) != f(f(z,w), u):
            c_holds = False
            break
    print(f"  C holds: {c_holds}")

print(f"\nTotal ops satisfying P: {count}")

print("\n" + "="*60)
print("Problem 1: Exhaustive on size 3, listing all ops satisfying P")
print("="*60)

count = 0
for t in product(S, repeat=SIZE*SIZE):
    table = {}
    for i in S:
        for j in S:
            table[(i,j)] = t[i*SIZE+j]

    def f(a,b):
        return table[(a,b)]

    p_holds = True
    for x,y in product(S, repeat=2):
        if x != f(y, f(f(y, f(y,x)), x)):
            p_holds = False
            break
    if not p_holds:
        continue

    count += 1
    print(f"\nOp #{count}:")
    for i in S:
        row = [f(i,j) for j in S]
        print(f"  f({i},*) = {row}")

    # Check C
    c_holds = True
    cx = None
    for x,y,z in product(S, repeat=3):
        if x != f(f(y, f(z,y)), f(y,x)):
            c_holds = False
            cx = (x,y,z)
            break
    if c_holds:
        print(f"  C holds: True")
    else:
        print(f"  C FAILS at {cx}")

print(f"\nTotal ops satisfying P: {count}")

# Problem 2: list all on size 3
print("\n" + "="*60)
print("Problem 2: Exhaustive on size 3, listing all ops satisfying P")
print("="*60)

count = 0
for t in product(S, repeat=SIZE*SIZE):
    table = {}
    for i in S:
        for j in S:
            table[(i,j)] = t[i*SIZE+j]

    def f(a,b):
        return table[(a,b)]

    p_holds = True
    for x,y,z in product(S, repeat=3):
        if f(x,y) != f(y, f(x, f(z,x))):
            p_holds = False
            break
    if not p_holds:
        continue

    count += 1
    print(f"\nOp #{count}:")
    for i in S:
        row = [f(i,j) for j in S]
        print(f"  f({i},*) = {row}")

    # Check C
    c_holds = True
    cx = None
    for x,y,z in product(S, repeat=3):
        if f(x,y) != f(f(y, f(z,x)), y):
            c_holds = False
            cx = (x,y,z)
            break
    if c_holds:
        print(f"  C holds: True")
    else:
        print(f"  C FAILS at {cx}")

print(f"\nTotal ops satisfying P: {count}")

# Problem 3: list all on size 3
print("\n" + "="*60)
print("Problem 3: Exhaustive on size 3, listing all ops satisfying P")
print("="*60)

count = 0
for t in product(S, repeat=SIZE*SIZE):
    table = {}
    for i in S:
        for j in S:
            table[(i,j)] = t[i*SIZE+j]

    def f(a,b):
        return table[(a,b)]

    p_holds = True
    for x,y,z in product(S, repeat=3):
        if x != f(f(f(f(y,y), x), x), z):
            p_holds = False
            break
    if not p_holds:
        continue

    count += 1
    print(f"\nOp #{count}:")
    for i in S:
        row = [f(i,j) for j in S]
        print(f"  f({i},*) = {row}")

print(f"\nTotal ops satisfying P: {count}")
