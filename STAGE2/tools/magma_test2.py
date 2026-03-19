from itertools import product
import sys

def test_on_size(n):
    """Test all problems on magmas of size n."""
    S = list(range(n))
    # Number of entries in multiplication table: n^2
    # Number of operations: n^(n^2)
    num_entries = n * n
    num_ops = n ** num_entries
    print(f"Testing on set of size {n}: {num_ops} operations, {num_entries} table entries")

    if num_ops > 500000:
        print(f"Too many operations ({num_ops}), skipping")
        return

    def make_op_from_index(idx):
        """Convert an integer index to a multiplication table."""
        table = {}
        for i in range(n):
            for j in range(n):
                table[(i, j)] = idx % n
                idx //= n
        return table

    def f(table, a, b):
        return table[(a, b)]

    # Problem 0: P: x*(y*z) = (y*w)*w, C: x*(y*y) = (z*w)*u
    print(f"\n--- Problem 0 (FALSE): P: x*(y*z)=(y*w)*w, C: x*(y*y)=(z*w)*u ---")
    count_p = 0
    for idx in range(num_ops):
        t = make_op_from_index(idx)
        # Check P universally
        p_ok = True
        for x in S:
            if not p_ok: break
            for y in S:
                if not p_ok: break
                for z in S:
                    if not p_ok: break
                    for w in S:
                        if f(t, x, f(t, y, z)) != f(t, f(t, y, w), w):
                            p_ok = False
                            break
        if not p_ok:
            continue
        count_p += 1
        # Check C universally
        c_ok = True
        ce = None
        for x in S:
            if not c_ok: break
            for y in S:
                if not c_ok: break
                for z in S:
                    if not c_ok: break
                    for w in S:
                        if not c_ok: break
                        for u in S:
                            if f(t, x, f(t, y, y)) != f(t, f(t, z, w), u):
                                c_ok = False
                                ce = (x, y, z, w, u)
                                break
        if not c_ok:
            print(f"  COUNTEREXAMPLE FOUND! Op index {idx}")
            print(f"  Table: {dict(sorted(t.items()))}")
            print(f"  C fails at: x={ce[0]}, y={ce[1]}, z={ce[2]}, w={ce[3]}, u={ce[4]}")
            lhs = f(t, ce[0], f(t, ce[1], ce[1]))
            rhs = f(t, f(t, ce[2], ce[3]), ce[4])
            print(f"  LHS = {lhs}, RHS = {rhs}")
            # Only need one counterexample
            print(f"  (Total ops satisfying P so far: {count_p})")
            break
    else:
        print(f"  No counterexample found. {count_p} ops satisfy P.")

    # Problem 1: P: x = y*((y*(y*x))*x), C: x = (y*(z*y))*(y*x)
    print(f"\n--- Problem 1 (FALSE): P: x=y*((y*(y*x))*x), C: x=(y*(z*y))*(y*x) ---")
    count_p = 0
    for idx in range(num_ops):
        t = make_op_from_index(idx)
        p_ok = True
        for x in S:
            if not p_ok: break
            for y in S:
                if x != f(t, y, f(t, f(t, y, f(t, y, x)), x)):
                    p_ok = False
                    break
        if not p_ok:
            continue
        count_p += 1
        c_ok = True
        ce = None
        for x in S:
            if not c_ok: break
            for y in S:
                if not c_ok: break
                for z in S:
                    if x != f(t, f(t, y, f(t, z, y)), f(t, y, x)):
                        c_ok = False
                        ce = (x, y, z)
                        break
        if not c_ok:
            print(f"  COUNTEREXAMPLE FOUND! Op index {idx}")
            print(f"  Table: {dict(sorted(t.items()))}")
            print(f"  C fails at: x={ce[0]}, y={ce[1]}, z={ce[2]}")
            lhs = ce[0]
            rhs = f(t, f(t, ce[1], f(t, ce[2], ce[1])), f(t, ce[1], ce[0]))
            print(f"  LHS = {lhs}, RHS = {rhs}")
            print(f"  (Total ops satisfying P so far: {count_p})")
            break
    else:
        print(f"  No counterexample found. {count_p} ops satisfy P.")

    # Problem 2: P: x*y = y*(x*(z*x)), C: x*y = (y*(z*x))*y
    print(f"\n--- Problem 2 (TRUE): P: x*y=y*(x*(z*x)), C: x*y=(y*(z*x))*y ---")
    count_p = 0
    for idx in range(num_ops):
        t = make_op_from_index(idx)
        p_ok = True
        for x in S:
            if not p_ok: break
            for y in S:
                if not p_ok: break
                for z in S:
                    if f(t, x, y) != f(t, y, f(t, x, f(t, z, x))):
                        p_ok = False
                        break
        if not p_ok:
            continue
        count_p += 1
        c_ok = True
        ce = None
        for x in S:
            if not c_ok: break
            for y in S:
                if not c_ok: break
                for z in S:
                    if f(t, x, y) != f(t, f(t, y, f(t, z, x)), y):
                        c_ok = False
                        ce = (x, y, z)
                        break
        if not c_ok:
            print(f"  COUNTEREXAMPLE for TRUE claim! Op index {idx}")
            print(f"  Table: {dict(sorted(t.items()))}")
            print(f"  C fails at: x={ce[0]}, y={ce[1]}, z={ce[2]}")
            break
    else:
        print(f"  No counterexample found (consistent with TRUE). {count_p} ops satisfy P.")

    # Problem 3: P: x = (((y*y)*x)*x)*z, C: x = y*((x*(y*z))*w)
    print(f"\n--- Problem 3 (TRUE): P: x=(((y*y)*x)*x)*z, C: x=y*((x*(y*z))*w) ---")
    count_p = 0
    for idx in range(num_ops):
        t = make_op_from_index(idx)
        p_ok = True
        for x in S:
            if not p_ok: break
            for y in S:
                if not p_ok: break
                for z in S:
                    if x != f(t, f(t, f(t, f(t, y, y), x), x), z):
                        p_ok = False
                        break
        if not p_ok:
            continue
        count_p += 1
        c_ok = True
        ce = None
        for x in S:
            if not c_ok: break
            for y in S:
                if not c_ok: break
                for z in S:
                    if not c_ok: break
                    for w in S:
                        if x != f(t, y, f(t, f(t, x, f(t, y, z)), w)):
                            c_ok = False
                            ce = (x, y, z, w)
                            break
        if not c_ok:
            print(f"  COUNTEREXAMPLE for TRUE claim! Op index {idx}")
            print(f"  Table: {dict(sorted(t.items()))}")
            print(f"  C fails at: x={ce[0]}, y={ce[1]}, z={ce[2]}, w={ce[3]}")
            break
    else:
        print(f"  No counterexample found (consistent with TRUE). {count_p} ops satisfy P.")

# Test size 2 first, then size 3
test_on_size(2)
test_on_size(3)
