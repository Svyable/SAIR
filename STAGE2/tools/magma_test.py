from itertools import product

# All 16 binary operations on {0,1}
# op is a tuple (f(0,0), f(0,1), f(1,0), f(1,1))
def make_op(bits):
    table = {(0,0): bits[0], (0,1): bits[1], (1,0): bits[2], (1,1): bits[3]}
    return lambda a, b: table[(a, b)]

all_ops = list(product([0,1], repeat=4))
S = [0, 1]

def op_str(bits):
    return f"f(0,0)={bits[0]} f(0,1)={bits[1]} f(1,0)={bits[2]} f(1,1)={bits[3]}"

def check_problem(name, premise_check, conclusion_check, var_counts_P, var_counts_C):
    """
    premise_check(f, assignment) -> bool: does premise hold for this assignment?
    conclusion_check(f, assignment) -> bool: does conclusion hold for this assignment?
    var_counts_P: number of free variables in P
    var_counts_C: number of free variables in C
    """
    print(f"\n{'='*60}")
    print(f"Problem: {name}")
    print(f"{'='*60}")

    ops_satisfying_P = []

    for bits in all_ops:
        f = make_op(bits)

        # Check if P holds universally (for all assignments of var_counts_P variables)
        p_holds = True
        for vals in product(S, repeat=var_counts_P):
            if not premise_check(f, vals):
                p_holds = False
                break

        if p_holds:
            # Check if C holds universally
            c_holds = True
            counterex = None
            for vals in product(S, repeat=var_counts_C):
                if not conclusion_check(f, vals):
                    c_holds = False
                    counterex = vals
                    break

            ops_satisfying_P.append((bits, c_holds, counterex))

    print(f"Operations where P holds universally: {len(ops_satisfying_P)}")

    all_imply = True
    for bits, c_holds, counterex in ops_satisfying_P:
        status = "C holds" if c_holds else f"C FAILS with assignment {counterex}"
        if not c_holds:
            all_imply = False
        print(f"  Op ({bits}): {status}")

    if all_imply:
        print(f"  => IMPLICATION HOLDS (no counterexample found on {{0,1}})")
    else:
        print(f"  => COUNTEREXAMPLE FOUND on {{0,1}}")

# Problem 0: P: x*(y*z) = (y*w)*w, C: x*(y*y) = (z*w)*u
# P has vars x,y,z,w (4), C has vars x,y,z,w,u (5)
def p0_premise(f, vals):
    x, y, z, w = vals
    return f(x, f(y, z)) == f(f(y, w), w)

def p0_conclusion(f, vals):
    x, y, z, w, u = vals
    return f(x, f(y, y)) == f(f(z, w), u)

check_problem("FALSE #0: P: x*(y*z)=(y*w)*w, C: x*(y*y)=(z*w)*u",
              p0_premise, p0_conclusion, 4, 5)

# Problem 1: P: x = y*((y*(y*x))*x), C: x = (y*(z*y))*(y*x)
# P has vars x,y (2), C has vars x,y,z (3)
def p1_premise(f, vals):
    x, y = vals
    return x == f(y, f(f(y, f(y, x)), x))

def p1_conclusion(f, vals):
    x, y, z = vals
    return x == f(f(y, f(z, y)), f(y, x))

check_problem("FALSE #1: P: x=y*((y*(y*x))*x), C: x=(y*(z*y))*(y*x)",
              p1_premise, p1_conclusion, 2, 3)

# Problem 2: P: x*y = y*(x*(z*x)), C: x*y = (y*(z*x))*y
# P has vars x,y,z (3), C has vars x,y,z (3)
def p2_premise(f, vals):
    x, y, z = vals
    return f(x, y) == f(y, f(x, f(z, x)))

def p2_conclusion(f, vals):
    x, y, z = vals
    return f(x, y) == f(f(y, f(z, x)), y)

check_problem("TRUE #2: P: x*y=y*(x*(z*x)), C: x*y=(y*(z*x))*y",
              p2_premise, p2_conclusion, 3, 3)

# Problem 3: P: x = (((y*y)*x)*x)*z, C: x = y*((x*(y*z))*w)
# P has vars x,y,z (3), C has vars x,y,z,w (4)
def p3_premise(f, vals):
    x, y, z = vals
    return x == f(f(f(f(y, y), x), x), z)

def p3_conclusion(f, vals):
    x, y, z, w = vals
    return x == f(y, f(f(x, f(y, z)), w))

check_problem("TRUE #3: P: x=(((y*y)*x)*x)*z, C: x=y*((x*(y*z))*w)",
              p3_premise, p3_conclusion, 3, 4)

# For Problem 3, let's also check if P forces all elements to be equal
print(f"\n{'='*60}")
print("Problem 3 analysis: Does P force a trivial (single-element) algebra on {0,1}?")
print(f"{'='*60}")
for bits in all_ops:
    f = make_op(bits)
    p_holds = True
    for vals in product(S, repeat=3):
        x, y, z = vals
        if not (x == f(f(f(f(y, y), x), x), z)):
            p_holds = False
            break
    if p_holds:
        # Check if 0 and 1 are forced equal (i.e., is the magma trivially {c} for some c?)
        # On {0,1}, "all elements equal" means the algebra only "uses" one value
        # Check: does f(a,b) = constant for all a,b?
        vals_produced = set(bits)
        print(f"  Op ({bits}): P holds. f values = {vals_produced}. ", end="")
        # Check if in any model of P on {0,1}, both 0 and 1 are actually reachable
        # Since our carrier is {0,1}, if P holds, let's see what happens
        if len(vals_produced) == 1:
            print("Constant operation - effectively trivial!")
        else:
            print("Non-constant - both elements distinguishable")
