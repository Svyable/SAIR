from itertools import product
import random

S2 = list(range(2))
S3 = list(range(3))

# Let's first understand what ops satisfy P for problems 0 and 1 on size 3
# and analyze their structure

def make_table(n, idx):
    table = {}
    for i in range(n):
        for j in range(n):
            table[(i, j)] = idx % n
            idx //= n
    return table

def f(t, a, b):
    return t[(a, b)]

def print_table(t, n):
    print("  * |", " ".join(str(j) for j in range(n)))
    print("  --+" + "--" * n)
    for i in range(n):
        row = " ".join(str(t[(i,j)]) for j in range(n))
        print(f"  {i} | {row}")

# Analyze problem 0 models on size 3
print("=== Problem 0: Models of P on {0,1,2} ===")
print("P: x*(y*z) = (y*w)*w")
n = 3
for idx in range(n**(n*n)):
    t = make_table(n, idx)
    p_ok = True
    for x in range(n):
        if not p_ok: break
        for y in range(n):
            if not p_ok: break
            for z in range(n):
                if not p_ok: break
                for w in range(n):
                    if f(t, x, f(t, y, z)) != f(t, f(t, y, w), w):
                        p_ok = False
                        break
    if p_ok:
        print(f"\nModel (idx={idx}):")
        print_table(t, n)
        # Check: is this a constant operation?
        vals = set(t.values())
        print(f"  Range of f: {vals}")
        # Check: is x*y = constant?
        is_const = len(vals) == 1
        print(f"  Constant op: {is_const}")

# Analyze problem 1 models on size 3
print("\n\n=== Problem 1: Models of P on {0,1,2} ===")
print("P: x = y*((y*(y*x))*x)")
for idx in range(n**(n*n)):
    t = make_table(n, idx)
    p_ok = True
    for x in range(n):
        if not p_ok: break
        for y in range(n):
            if x != f(t, y, f(t, f(t, y, f(t, y, x)), x)):
                p_ok = False
                break
    if p_ok:
        print(f"\nModel (idx={idx}):")
        print_table(t, n)
        vals = set(t.values())
        print(f"  Range of f: {vals}")

# For problem 0, let's check: does P force x*y to only depend on x (or only on y)?
# Or maybe P forces the operation to be a "left zero" or "right zero" band?
# Let's also check models on size 2
print("\n\n=== Problem 0: Models of P on {0,1} ===")
n = 2
for idx in range(n**(n*n)):
    t = make_table(n, idx)
    p_ok = True
    for x in range(n):
        if not p_ok: break
        for y in range(n):
            if not p_ok: break
            for z in range(n):
                if not p_ok: break
                for w in range(n):
                    if f(t, x, f(t, y, z)) != f(t, f(t, y, w), w):
                        p_ok = False
                        break
    if p_ok:
        print(f"\nModel (idx={idx}):")
        print_table(t, n)

print("\n\n=== Problem 1: Models of P on {0,1} ===")
for idx in range(n**(n*n)):
    t = make_table(n, idx)
    p_ok = True
    for x in range(n):
        if not p_ok: break
        for y in range(n):
            if x != f(t, y, f(t, f(t, y, f(t, y, x)), x)):
                p_ok = False
                break
    if p_ok:
        print(f"\nModel (idx={idx}):")
        print_table(t, n)
