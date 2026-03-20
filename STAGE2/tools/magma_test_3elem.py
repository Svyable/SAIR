from itertools import product

S = [0, 1, 2]
SIZE = len(S)

def make_op_from_tuple(t):
    """t has SIZE*SIZE entries: t[i*SIZE+j] = f(i,j)"""
    table = {}
    for i in S:
        for j in S:
            table[(i,j)] = t[i*SIZE+j]
    return table

def f(op, a, b):
    return op[(a,b)]

# Too many ops on 3 elements (3^9 = 19683). We'll iterate.
# For efficiency, generate tuples on the fly.

def check_problem_3elem(name, premise_check, conclusion_check, nvars_P, nvars_C):
    print(f"\n{'='*60}")
    print(f"Problem: {name}")
    print(f"{'='*60}")

    count_P = 0
    found_counterex = False

    for t in product(S, repeat=SIZE*SIZE):
        op = make_op_from_tuple(t)

        # Check P universally
        p_holds = True
        for vals in product(S, repeat=nvars_P):
            if not premise_check(op, vals):
                p_holds = False
                break

        if not p_holds:
            continue

        count_P += 1

        # Check C universally
        for vals in product(S, repeat=nvars_C):
            if not conclusion_check(op, vals):
                print(f"  COUNTEREXAMPLE FOUND!")
                print(f"  Operation table: {t}")
                print(f"  f(i,j) table:")
                for i in S:
                    row = [f(op,i,j) for j in S]
                    print(f"    f({i},*) = {row}")
                print(f"  C fails at assignment {vals}")
                found_counterex = True
                break

        if found_counterex:
            break

    if not found_counterex:
        print(f"  No counterexample found. {count_P} ops satisfy P.")

    return found_counterex

# Problem 0: P: x*(y*z) = (y*w)*w, C: x*(y*y) = (z*w)*u
def p0_P(op, vals):
    x,y,z,w = vals
    return f(op,x,f(op,y,z)) == f(op,f(op,y,w),w)
def p0_C(op, vals):
    x,y,z,w,u = vals
    return f(op,x,f(op,y,y)) == f(op,f(op,z,w),u)

# Problem 1: P: x = y*((y*(y*x))*x), C: x = (y*(z*y))*(y*x)
def p1_P(op, vals):
    x,y = vals
    return x == f(op,y,f(op,f(op,y,f(op,y,x)),x))
def p1_C(op, vals):
    x,y,z = vals
    return x == f(op,f(op,y,f(op,z,y)),f(op,y,x))

print("Testing on 3-element magmas (this may take a while)...")

check_problem_3elem("FALSE #0: P: x*(y*z)=(y*w)*w, C: x*(y*y)=(z*w)*u",
                    p0_P, p0_C, 4, 5)

check_problem_3elem("FALSE #1: P: x=y*((y*(y*x))*x), C: x=(y*(z*y))*(y*x)",
                    p1_P, p1_C, 2, 3)
