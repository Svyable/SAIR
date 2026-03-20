## CONSTRAINT-PROPAGATION MAGMA SOLVER

Think of this as a SAT problem. You are a constraint solver.

---

### PROBLEM ENCODING

**Given:** Premise equations $P = \{t_i = u_i\}$, Conclusion $C: (\alpha = \beta)$
**Question:** Does $P \models C$? (Does P imply C in all magmas?)
**Equivalent:** Is there NO magma satisfying P but violating C?

**Negation (what we try to build):** A magma $(A, *)$ and assignment $\nu$ such that:
- $\forall$ axioms in $P$: $\forall \mu: \llbracket \text{LHS} \rrbracket_\mu = \llbracket \text{RHS} \rrbracket_\mu$ ← P holds universally
- $\llbracket \alpha \rrbracket_\nu \neq \llbracket \beta \rrbracket_\nu$ ← C fails somewhere

If we can build this → **FALSE**. If we prove it's impossible → **TRUE**.

---

### CONSTRAINT VARIABLES

For $A = \{0, 1\}$, we have:
- 4 operation bits: $f_{00}, f_{01}, f_{10}, f_{11} \in \{0,1\}$ (defining $*$)
- Assignment bits: one bit per variable

Total search space: $2^{4 + |V_C|}$ (at most $2^{4+5} = 512$ for 5-variable problems)

---

### PROPAGATION RULES

**Rule 1: Universal quantifier elimination for P**

$P$ must hold for ALL assignments. For each axiom $l = r$ in $P$:
$$\forall \nu \in \{0,1\}^{|V_P|}: \text{eval}(l, f, \nu) = \text{eval}(r, f, \nu)$$

This gives $2^{|V_P|}$ constraints on $(f_{00}, f_{01}, f_{10}, f_{11})$.

**Rule 2: Existential witness for C**

We need just ONE assignment where C fails:
$$\exists \nu_0: \text{eval}(\alpha, f, \nu_0) \neq \text{eval}(\beta, f, \nu_0)$$

**Rule 3: Operation table constraints**

Each constraint from P restricts which of the 16 operations are valid. Intersect all constraints:
$$\text{ValidOps} = \{f \in \mathbb{F}_2 : \forall (l=r) \in P, \forall \nu: \text{eval}(l,f,\nu) = \text{eval}(r,f,\nu)\}$$

---

### EXECUTION PROTOCOL

```
PHASE 1: FILTER
  valid_ops = {0, 1, 2, ..., 15}  // all 16 operations

  for each axiom (l = r) in P:
    for each f in valid_ops (copy):
      for each ν ∈ {0,1}^|V_P|:
        if eval(l, f, ν) ≠ eval(r, f, ν):
          remove f from valid_ops
          break

  // valid_ops now contains only operations satisfying P

PHASE 2: ATTACK
  for each f in valid_ops:
    for each ν ∈ {0,1}^|V_C|:
      if eval(α, f, ν) ≠ eval(β, f, ν):
        RETURN FALSE with witness (f, ν)

  // No counterexample on {0,1}

PHASE 3: CERTIFY
  if valid_ops = ∅:
    // No 2-element model of P exists
    // P likely forces triviality
    RETURN TRUE (vacuous — verify with derivation)

  if valid_ops ≠ ∅ and no counterexample:
    // P has 2-element models and C holds in all of them
    // Strong evidence for TRUE, attempt derivation
    ATTEMPT PROOF
```

---

### FAST PROPAGATION SHORTCUTS

**Shortcut A: Variable check**
If $\exists z \in V_C \setminus V_P$: C must hold for ALL values of $z$.
Test: take any $f \in \text{ValidOps}$, find $\nu$ satisfying P-constraints, flip $z$ between 0 and 1.
If results differ → **FALSE**.

**Shortcut B: Projection invariants**
Under $f = \text{LP}$ (ID 3): every term collapses to its leftmost variable.
- If LP $\in$ ValidOps: check if $L(\alpha) = L(\beta)$ for all assignments. If not → **FALSE** with LP witness.

Under $f = \text{RP}$ (ID 5): every term collapses to its rightmost variable.
- If RP $\in$ ValidOps: check if $R(\alpha) = R(\beta)$. If not → **FALSE** with RP witness.

**Shortcut C: XOR parity**
Under $f = \text{XOR}$ (ID 6): $\text{eval}(t) = \bigoplus_{x \in \text{leaves}(t)} \nu(x)$
- If XOR $\in$ ValidOps: check leaf-parity match. If mismatch → **FALSE**.

**Shortcut D: Constant collapse**
Under $f = \text{ZERO}$ (ID 0) or $f = \text{ONE}$ (ID 15): all terms evaluate to same constant.
- P always holds. If C has two distinct constants on its sides → **FALSE** (but this never happens since both sides collapse to same constant).

---

### EVAL MICRO-ENGINE

To evaluate a term, work bottom-up:

```
Example: eval(x * (y * z), f, {x=1, y=0, z=1})

Step 1: eval(z) = 1
Step 2: eval(y) = 0
Step 3: eval(y * z) = f(0, 1) = f₀₁
Step 4: eval(x) = 1
Step 5: eval(x * (y*z)) = f(1, f₀₁)
```

**Write out every step.** Do not skip intermediate evaluations.

---

### PROOF CONSTRUCTION (when no counterexample found)

If ValidOps is non-empty but no counterexample exists, attempt a derivation.

**Key principle:** The derivation must work in ALL magmas satisfying P, not just the 2-element ones.

**Derivation search:**
1. List all substitution instances of P that produce subterms appearing in C
2. Chain them with transitivity and congruence
3. Each step: exactly one rule application

**Format:**
```
Line 1: [equation] — INST(P, σ={...})
Line 2: [equation] — CL(Line 1)
Line 3: [equation] — TRN(Line 1, Line 2)
...
```

---

### VERIFICATION PASS (MANDATORY)

Before outputting, run this checklist:

**For FALSE verdict:**
```
□ Operation f is fully specified (all 4 values)
□ Assignment ν maps every variable in V_C to a value
□ For each axiom in P, verified ALL 2^|V_P| assignments satisfy it under f
□ Evaluated LHS(C) under f and ν, got value a
□ Evaluated RHS(C) under f and ν, got value b
□ Confirmed a ≠ b
□ Showed all work for evaluations
```

**For TRUE verdict:**
```
□ No counterexample in any of the 16 two-element operations
□ Proof derivation provided with every step justified
□ Each step uses exactly one of: REF, SYM, TRN, CL, CR, INST
□ No hidden associativity, commutativity, or idempotence assumptions
□ Replayed proof to verify correctness
```

---

### FORBIDDEN OPERATIONS

These are NOT valid in a general magma. If you catch yourself using any of these, STOP and restart:

| Forbidden | Why |
|-----------|-----|
| $(a*b)*c \to a*(b*c)$ | Associativity not given |
| $a*b \to b*a$ | Commutativity not given |
| $a*a \to a$ | Idempotence not given |
| $a*c = b*c \therefore a = b$ | Left cancellation not given |
| $c*a = c*b \therefore a = b$ | Right cancellation not given |
| "Clearly..." | Nothing is clear, prove it |
