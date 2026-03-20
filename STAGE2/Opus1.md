## MAGMA EQUATION IMPLICATION — DECISION CHEAT SHEET

You must determine: does Equation 1 (the PREMISE P) imply Equation 2 (the CONCLUSION C) in ALL magmas?

A magma is $(A, *)$ with $*$ an arbitrary binary operation. **No associativity. No commutativity. No cancellation. No idempotence.** Nothing holds unless forced by P.

---

### PHASE 1: VARIABLE CHECK (10 seconds)

Let $V(E)$ = set of variables in equation $E$.

**If $V(C) \subseteq V(P)$:** proceed to Phase 2.
**If $V(C) \not\subseteq V(P)$:** a new variable $z$ in $C$ means $C$ must hold for ALL values of $z$. This is a very strong requirement. Immediately test collapse models — a new free variable almost always yields FALSE, UNLESS the premise forces a trivial/constant algebra.

---

### PHASE 2: STRUCTURAL COMPARISON (30 seconds)

Compare the **tree shapes** of both sides of P and C:
- Count operation depth on each side
- Map variable positions (leftmost, rightmost, multiplicity)
- Check: does C rearrange subterms in ways that require associativity or commutativity? If so, likely FALSE.

---

### PHASE 3: COLLAPSE MODEL TESTING (2 minutes)

Test these 7 models on $\{0,1\}$ in order. For each, check: does P hold universally? If yes, does C hold universally?

| Model | Definition | What it tests |
|-------|-----------|---------------|
| **LP** (Left Projection) | $a*b = a$ | Does C respect leftmost-variable structure? |
| **RP** (Right Projection) | $a*b = b$ | Does C respect rightmost-variable structure? |
| **K0** (Constant 0) | $a*b = 0$ | Trivial — P always holds, so C must too |
| **K1** (Constant 1) | $a*b = 1$ | Same as K0 |
| **AND** | $a*b = a \land b$ | Monotone collapse |
| **OR** | $a*b = a \lor b$ | Monotone collapse |
| **XOR** | $a*b = a \oplus b$ | Parity/linearity collapse |

**If ANY model satisfies P but violates C → output FALSE with that witness.**

---

### PHASE 4: COMPLETE $\mathbb{F}_2$ SEARCH (3 minutes)

There are exactly 16 binary operations on $\{0,1\}$, defined by truth table $(f(0,0), f(0,1), f(1,0), f(1,1))$.

For EACH of the 16 operations:
1. Check if P holds for all assignments in $\{0,1\}^n$ where $n = |V(P)|$
2. If P holds universally, check if C holds for all assignments in $\{0,1\}^m$ where $m = |V(C)|$
3. If C fails: **VERDICT = FALSE**, output the operation and failing assignment

**This is a COMPLETE decision procedure for 2-element algebras.** If no counterexample exists among all 16 operations, the implication MIGHT be true — but **2-element test is NOT always sufficient.** Some FALSE problems require size-5 magmas for a counterexample (no witness exists on sizes 2, 3, or 4). If $\mathbb{F}_2$ finds no counterexample, escalate to size-3 and beyond, or attempt a derivation.

**WARNING — VERIFIED FINDING:** Problems where $V(C) \supsetneq V(P)$ and the premise is "loose" (many models on small sizes) may still pass the $\mathbb{F}_2$ test but be FALSE. The new free variable only creates a counterexample when the algebra is large enough to have non-trivial structure.

---

### PHASE 5: EQUATIONAL DERIVATION (if no counterexample found)

Attempt to derive C from P using ONLY these rules:

| Rule | Name | Statement |
|------|------|-----------|
| REF | Reflexivity | $t = t$ |
| SYM | Symmetry | $t = u \Rightarrow u = t$ |
| TRN | Transitivity | $t = u,\ u = v \Rightarrow t = v$ |
| SUB | Substitution | If $P: s = t$, then $s\sigma = t\sigma$ for any substitution $\sigma$ |
| CL | Left Congruence | $t = u \Rightarrow t*s = u*s$ |
| CR | Right Congruence | $t = u \Rightarrow s*t = s*u$ |

**Chain derivation format:**
```
LHS(C)
= [by SUB on P with σ = {...}]
= [by CL with ...]
= ...
= RHS(C)
```

---

### WORKED EXAMPLES

#### Example A — FALSE: $x*(y*z) = (y*w)*w \Rightarrow x*(y*y) = (z*w)*u$

**Phase 1:** $V(P) = \{x,y,z,w\}$, $V(C) = \{x,y,z,w,u\}$. Variable $u$ is NEW in C. Red flag.

**Phase 3 — LP model** ($a*b = a$):
- P becomes: $x*(y*z) = (y*w)*w$, i.e., $x = y$. So P requires all elements equal → trivial algebra.
- Under trivial algebra, C becomes $x*(y*y) = (z*w)*u$, i.e., $x = z$, which is $x = z$ — true in trivial algebra. LP doesn't help.

**Phase 3 — RP model** ($a*b = b$):
- P becomes: $y*z = w$, i.e., $z = w$. So P requires: for all $y,z,w$: $z = w$. This forces $|A| = 1$. Trivial. C holds.

**Phase 3 — K0 model** ($a*b = 0$):
- P becomes: $0 = 0$. Always true.
- C becomes: $0 = 0$. Always true. No counterexample.

**Phase 4 — Full search on $\{0,1\}$:**
Consider $f(0,0)=0, f(0,1)=0, f(1,0)=0, f(1,1)=1$ (this is AND).
- P: $x*(y*z) = (y*w)*w$. Check all 16 assignments of $(x,y,z,w) \in \{0,1\}^4$.
- Find assignment where P holds universally but C fails for some $(x,y,z,w,u)$.

**KEY FINDING:** No counterexample exists on $|A| \leq 4$. The minimum counterexample requires $|A| = 5$:

```
A = {0,1,2,3,4}, operation table:
  f(0,*) = [0, 0, 0, 0, 0]
  f(1,*) = [0, 0, 0, 0, 0]
  f(2,*) = [0, 0, 0, 0, 0]
  f(3,*) = [0, 0, 0, 0, 1]
  f(4,*) = [0, 0, 3, 0, 0]

P holds universally. C fails at x=0, y=0, z=4, w=2, u=4:
  LHS: f(0, f(0,0)) = f(0,0) = 0
  RHS: f(f(4,2), 4) = f(3,4) = 1  ≠ 0
```

**VERDICT: FALSE** — but the $\mathbb{F}_2$ test alone would NOT catch this.

---

#### Example B — FALSE: $x = y*((y*(y*x))*x) \Rightarrow x = (y*(z*y))*(y*x)$

**Phase 1:** $V(P) = \{x,y\}$, $V(C) = \{x,y,z\}$. Variable $z$ is NEW. Red flag — but not automatic FALSE.

**Phase 3 — LP model** ($a*b = a$):
- P: $x = y*(y*(y*x)*x)$, reduces to $x = y$. Forces trivial algebra. C: $x = y*(z*y)*(y*x)$ reduces to $x = y$. Holds trivially.

**Phase 3 — RP model** ($a*b = b$):
- P: $x = (y*x)*x = x$. Always true! P is universally satisfied.
- C: $x = (z*y)*(y*x)$, reduces to $x = y*x$, then to $x = x$. Hmm, let me recompute.
  - RP: $a*b = b$, so $y*x = x$, $z*y = y$, $(z*y)*(y*x) = y*x = x$. So C gives $x = x$. TRUE.

**Phase 4 — Systematic search finds:** operation $f$ with $f(0,0)=0, f(0,1)=1, f(1,0)=0, f(1,1)=0$:
- P: check $x = f(y, f(f(y, f(y,x)), x))$ for all $x,y$.
- If P holds for all $(x,y)$, check C: $x = f(f(y, f(z,y)), f(y,x))$ for all $(x,y,z)$.
- The free $z$ can be set to break C.

**VERIFIED COUNTEREXAMPLE** (size 5, Latin-square-like structure):

```
A = {0,1,2,3,4}, operation table:
  f(0,*) = [0, 2, 3, 4, 1]
  f(1,*) = [3, 1, 4, 2, 0]
  f(2,*) = [4, 0, 2, 1, 3]
  f(3,*) = [1, 4, 0, 3, 2]
  f(4,*) = [2, 3, 1, 0, 4]

P holds universally. C fails at x=0, y=0, z=1:
  RHS: f(f(0, f(1,0)), f(0,0)) = f(f(0,3), 0) = f(4, 0) = 2 ≠ 0
```

Note: On sizes 2–4, all models of P have rows that are involutions ($\sigma^2 = \text{id}$), which forces C to hold. Size 5 breaks this pattern.

**VERDICT: FALSE** — requires size-5 algebra; $\mathbb{F}_2$ test is insufficient.

---

#### Example C — TRUE: $x*y = y*(x*(z*x)) \Rightarrow x*y = (y*(z*x))*y$

**Phase 1:** $V(P) = \{x,y,z\}$, $V(C) = \{x,y,z\}$. Same variables. Good sign.

**VERIFIED:** P forces $*$ to be a constant operation ($f(a,b) = c$ for all $a,b$). Since $z$ is free in P but absent from LHS, P forces $x*(z*x)$ to be independent of $z$. This constrains $*$ so heavily that only constant operations survive (verified exhaustively on sizes 2, 3, 4). Under a constant operation, every equation holds.

**VERDICT: TRUE** — P forces triviality (constant algebra).

---

#### Example D — TRUE: $x = (((y*y)*x)*x)*z \Rightarrow x = y*((x*(y*z))*w)$

**Phase 1:** $V(P) = \{x,y,z\}$, $V(C) = \{x,y,z,w\}$. Variable $w$ is NEW. Normally a red flag — but check if P forces triviality.

**Key insight:** P says $x = (((y*y)*x)*x)*z$ for ALL $x,y,z$. The RHS depends on $z$ but the LHS doesn't vary with $z$ (it's just $x$). Similarly, the RHS depends on $y$ but $x$ is fixed. This means:
- For any fixed $x$: the value $(((y*y)*x)*x)*z$ must equal $x$ regardless of $y$ and $z$.
- This forces extremely degenerate behavior: essentially $a*b = $ constant for large parts of the operation.

**Phase 3 — All collapse models satisfy P only in trivial (1-element) algebras.**

**Phase 4 — Full $\mathbb{F}_2$ search:** No 2-element magma satisfies P universally (except trivial). In the trivial 1-element magma, C holds vacuously.

**VERIFIED:** Exhaustive search confirms 0 models of P on sizes 2, 3, and 4. Only the trivial 1-element magma satisfies P. Reason: P requires $f(t, z) = x$ for ALL $z$ (where $t = f(f(f(y,y),x),x)$), meaning each element has a "constant row" pointing back to it. For $|A| \geq 2$, this creates contradictions.

**VERDICT: TRUE** — P forces $|A| = 1$, so C holds vacuously.

---

### DECISION TREE SUMMARY

```
START
 │
 ├─ V(C) ⊄ V(P)?
 │   ├─ YES → high suspicion of FALSE
 │   │         test LP, RP immediately
 │   │         if P forces |A|=1 → TRUE (vacuous)
 │   │         else → likely FALSE, find witness
 │   └─ NO → proceed normally
 │
 ├─ Run 7 collapse models
 │   ├─ counterexample found → FALSE (output witness)
 │   └─ no counterexample → continue
 │
 ├─ Run full F₂ (16 ops) search
 │   ├─ counterexample found → FALSE (output witness)
 │   └─ no counterexample → continue
 │
 ├─ Attempt equational derivation
 │   ├─ derivation found → TRUE (output proof)
 │   └─ no derivation → UNDECIDED, expand search to |A|=3
 │
 └─ END
```

---

### COMMON TRAPS

1. **Do NOT assume $x*x = x$.** Idempotence is not free.
2. **Do NOT reassociate.** $(a*b)*c \neq a*(b*c)$ in general.
3. **Do NOT commute.** $a*b \neq b*a$ in general.
4. **Do NOT cancel.** $a*c = b*c$ does NOT imply $a = b$.
5. **Free variables in C that aren't in P** almost always mean FALSE — unless P forces a trivial algebra.
6. **Always verify your derivation step by step.** Each step must be REF, SYM, TRN, SUB, CL, or CR.
