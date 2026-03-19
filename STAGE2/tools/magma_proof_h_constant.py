"""
Proving h is constant for Problem 0.

P: f(x, f(y,z)) = f(f(y,w), w) for all x,y,z,w.

We know:
- h(y) := f(f(y,w),w) is independent of w  [set two different w's in P]
- f(x, f(y,z)) = h(y) for all x,y,z  [from P]
- g(t) := f(x,t) for t in Im(f), independent of x  [since LHS of P doesn't depend on x]

Claim: h is constant.

Proof:
From P: f(x, f(y,z)) = h(y).

Now substitute y -> f(a,b) (which is a valid substitution since y is universally quantified):
f(x, f(f(a,b), z)) = h(f(a,b)).

But f(f(a,b), z) is just some element of S. Call it s.
The LHS is f(x, s). If s is in Im(f), then f(x, s) = g(s).

Actually s = f(f(a,b), z) IS in Im(f) (it's the value of f at (f(a,b), z)).
So f(x, s) = g(s). And g(s) = h(f(a,b)) by the equation above.

But also, s = f(f(a,b), z) = f(t, z) where t = f(a,b).
From P with x=t: f(t, f(y,z)) = h(y) for all y,z.
Wait, that's P applied with first argument t. But P says f(x, f(y,z)) = h(y),
so f(t, f(y,z)) = h(y). This tells us about f(t, Im(f)).

Hmm, let me try differently.

h(y) = f(f(y,w), w) for any w.
h(f(a,b)) = f(f(f(a,b), w), w) for any w.

From P (with y replaced by f(a,b)):
f(x, f(f(a,b), z)) = h(f(a,b)) for all x,z.

Now I want to connect h(f(a,b)) back to h(a) or something.

From the original P: f(x, f(a,z)) = h(a) for all x,z.
Set z=b: f(x, f(a,b)) = h(a).

So g(f(a,b)) = h(a) for all a,b.  ... (*)

Now: h(y) = f(f(y,w), w) = g(f(y,w)) [since f(y,w) in Im(f), f(x,f(y,w))=g(f(y,w))].
Wait: g(t) = f(x,t) for t in Im(f). And h(y) = f(x, f(y,z)) = g(f(y,z)).
But from (*): g(f(y,z)) = h(y). So h(y) = h(y). Circular.

Try: from (*), g(f(a,b)) = h(a).
Now h(f(a,b)) = g(f(f(a,b), z)) for any z [since h(c) = g(f(c,z)) for any z].
And g(f(f(a,b), z)) = h(f(a,b)) [by (*) with a -> f(a,b)].
Again circular.

Let me try substitution into h directly.
h(y) = f(f(y,w), w).
Set w = y: h(y) = f(f(y,y), y).
Set w = 0: h(y) = f(f(y,0), 0).

Now: h(h(y)).
h(h(y)) = f(f(h(y), w), w) = f(f(h(y), 0), 0).
From (*): g(f(a,b)) = h(a), and h(y) = g(f(y,z)).
h(h(y)) = g(f(h(y), z)) for any z. And g(f(h(y), z)) = h(h(y)). Circular again.

The issue is that all our equations involve g composed with f, and g(f(a,b)) = h(a),
so we keep going in circles.

NEW IDEA: Use (*): g(f(a,b)) = h(a).
This means: for any s in Im(f), g(s) = h(a) for ANY a such that f(a,b) = s for some b.
In other words, g(s) = h(a) for all a in the "first-coordinate preimage" of s.

So if s = f(a1, b1) = f(a2, b2), then h(a1) = g(s) = h(a2).
That means: h(a1) = h(a2) whenever there exist b1, b2 with f(a1, b1) = f(a2, b2).

Define the relation: a1 ~ a2 iff Im(f(a1,-)) ∩ Im(f(a2,-)) != empty.
Then h is constant on equivalence classes of the transitive closure of ~.

In fact: f(a, a) is in Im(f(a,-)) for all a. And we showed that
f(a, something) could overlap with f(a', something).

If the transitive closure of ~ is all of S, then h is constant.

But is that always true? What if there's a partition of S such that
Im(f(a,-)) and Im(f(b,-)) are disjoint for a, b in different parts?

From P: f(x, f(y,z)) = h(y). Set y=a: f(x, f(a,z)) = h(a).
f(a,z) ranges over Im(f(a,-)). For any t in Im(f(a,-)), g(t) = h(a).

If a1 ~ a2 via t (i.e., t in Im(f(a1,-)) ∩ Im(f(a2,-))),
then h(a1) = g(t) = h(a2). Good.

But what if Im(f(a,-)) and Im(f(b,-)) are disjoint?
Then g maps Im(f(a,-)) to h(a) and Im(f(b,-)) to h(b),
and h(a) != h(b) is possible.

BUT: consider h(a). h(a) = f(f(a,w),w) for any w.
f(a,w) in Im(f(a,-)). Call it t. f(t,w) = h(a).
So t is in Im(f(a,-)) and w is in Im(f(t,-))... wait:
f(t,w) doesn't tell us about Im(f(t,-)).
t = f(a,w), and f(t,w) = h(a). So w = w, and f(t,w) = h(a).
This means h(a) is in Im(f(t,-)) (specifically f(t,w) = h(a)).
And t is in Im(f(a,-)).

Now consider h(h(a)). h(h(a)) is well-defined.
h(h(a)) = g(f(h(a), z)) for any z. And g(f(h(a),z)) = h(h(a)).

Also: h(a) = f(t,w) where t = f(a,w). So h(a) is in Im(f(t,-)) ⊂ Im(f).
So h(a) is in Im(f). Then g(h(a)) = f(x, h(a)) for any x.

From P: f(x, f(y,z)) = h(y). Is h(a) = f(y,z) for some y,z? Yes, since h(a) is in Im(f).
Say h(a) = f(c,d). Then f(x, h(a)) = f(x, f(c,d)) = h(c).
So g(h(a)) = h(c) where h(a) = f(c,d).

But h(a) = f(c,d) means c satisfies f(c,d) = h(a). And g(h(a)) = h(c).
From (*): g(f(c,d)) = h(c). And f(c,d) = h(a). So g(h(a)) = h(c).

Now, h(a) is also = f(a', w) for a' = a (take w such that f(a,w) = t and f(t,w)=h(a)...
actually h(a) = f(f(a,w),w).) So h(a) = f(t, w) where t = f(a,w).
From (*): g(f(t,w)) = h(t). And f(t,w) = h(a). So g(h(a)) = h(t) = h(f(a,w)).

So h(f(a,w)) = g(h(a)) for all a,w.

And h(c) = g(h(a)) when h(a) = f(c,d). But h(a) = f(f(a,w),w) = f(t,w) with t=f(a,w).
So c = t = f(a,w), d = w. And h(c) = h(f(a,w)).

So: h(f(a,w)) = g(h(a)) for all a, w.

Now: g(h(a)) = f(x, h(a)) for any x. And h(a) = f(f(a,w),w).
Set y = f(a,w) in the identity f(x, f(y,z)) = h(y):
f(x, f(f(a,w), z)) = h(f(a,w)).
Set z = w: f(x, f(f(a,w), w)) = h(f(a,w)).
f(x, h(a)) = h(f(a,w)).
So g(h(a)) = h(f(a,w)).

And from above: h(f(a,w)) = g(h(a)). Consistent.

Now: from g(h(a)) = h(f(a,w)) for ALL w:
h(f(a,w1)) = h(f(a,w2)) for all w1, w2.
So h is constant on Im(f(a,-)) for each a. This we already knew.

BREAKTHROUGH ATTEMPT:
h(f(a,w)) = g(h(a)).
The RHS doesn't depend on w. OK, we knew that.
But it also doesn't depend on a and w INDEPENDENTLY -- only through h(a).

Now: g(h(a)) = h(f(a,w)).
RHS is h applied to an element of Im(f(a,-)).
For any b in Im(f(a,-)), h(b) = g(h(a)).

Now suppose we have a1, a2 with h(a1) = h(a2). Then g(h(a1)) = g(h(a2)),
so h(b) is the same for b in Im(f(a1,-)) or Im(f(a2,-)).

What about a1, a2 with h(a1) != h(a2)?
Then g(h(a1)) != g(h(a2)) [unless g maps both to the same value].
Wait, could g(h(a1)) = g(h(a2)) even if h(a1) != h(a2)?

g is defined on Im(f). Are h(a1), h(a2) both in Im(f)? Yes (shown above).
g(h(a1)) = h(c) where h(a1) = f(c,d). Different h(a1) might map to different
or same values under g.

This is getting complex. Let me check computationally: in the size-4 models,
is there one where Im(f) != S?
"""

from itertools import product

S = [0,1,2,3]
SIZE = 4
f_table = [[None]*SIZE for _ in range(SIZE)]

solutions = []

def backtrack(pos):
    if len(solutions) >= 200:
        return
    if pos == SIZE * SIZE:
        for x,y,z,w in product(S, repeat=4):
            if f_table[x][f_table[y][z]] != f_table[f_table[y][w]][w]:
                return
        solutions.append([row[:] for row in f_table])
        return
    a, b = pos // SIZE, pos % SIZE
    for v in S:
        f_table[a][b] = v
        feasible = True
        for x,y,z,w in product(S, repeat=4):
            yz = f_table[y][z] if f_table[y][z] is not None else -1
            yw = f_table[y][w] if f_table[y][w] is not None else -1
            if yz == -1 or yw == -1: continue
            lhs = f_table[x][yz] if f_table[x][yz] is not None else -1
            rhs = f_table[yw][w] if f_table[yw][w] is not None else -1
            if lhs == -1 or rhs == -1: continue
            if lhs != rhs:
                feasible = False
                break
        if feasible:
            backtrack(pos + 1)
    f_table[a][b] = None

backtrack(0)
print(f"Found {len(solutions)} models on size 4")

for sol in solutions:
    im = set()
    for i in S:
        for j in S:
            im.add(sol[i][j])
    if im != set(S):
        print(f"  Non-surjective! Im={im}, table:")
        for i in S:
            print(f"    f({i},*) = {sol[i]}")

        # Check: is h constant?
        h_vals = set()
        for y in S:
            hy = sol[sol[y][0]][0]  # w=0
            h_vals.add(hy)
        print(f"    h values: {h_vals}")

        # Check what f(Im(f), u) looks like for u not in Im(f)
        non_im = set(S) - im
        for u in non_im:
            f_im_u = set()
            for s in im:
                f_im_u.add(sol[s][u])
            print(f"    f(Im(f), {u}) = {f_im_u}")

print("\nDone.")
