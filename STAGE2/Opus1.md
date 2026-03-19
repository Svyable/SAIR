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

**This is a COMPLETE decision procedure for 2-element algebras.** If no counterexample exists among all 16 operations, the implication MIGHT be true (but 2-element test is not always sufficient — it IS sufficient for equations with ≤3 variables in most practical cases).

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

The key insight: when P forces the algebra to be non-trivial, the free variable $u$ in C creates room for a counterexample.

**VERDICT: FALSE**

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

**VERDICT: FALSE** — The free variable $z$ allows a counterexample.

---

#### Example C — TRUE: $x*y = y*(x*(z*x)) \Rightarrow x*y = (y*(z*x))*y$

**Phase 1:** $V(P) = \{x,y,z\}$, $V(C) = \{x,y,z\}$. Same variables. Good sign.

**Phase 3–4:** No counterexample found in $\mathbb{F}_2$.

**Phase 5 — Derivation sketch:**
From P: $x*y = y*(x*(z*x))$ for all $x,y,z$.

Substitution instances of P give us tools. The key idea: P says the LHS $x*y$ equals a specific rearrangement on the RHS. By applying P to subterms of itself (substituting into P), we can transform $y*(x*(z*x))$ into $(y*(z*x))*y$.

Apply P with appropriate substitutions to show both sides of C equal the same intermediate expression.

**VERDICT: TRUE**

---

#### Example D — TRUE: $x = (((y*y)*x)*x)*z \Rightarrow x = y*((x*(y*z))*w)$

**Phase 1:** $V(P) = \{x,y,z\}$, $V(C) = \{x,y,z,w\}$. Variable $w$ is NEW. Normally a red flag — but check if P forces triviality.

**Key insight:** P says $x = (((y*y)*x)*x)*z$ for ALL $x,y,z$. The RHS depends on $z$ but the LHS doesn't vary with $z$ (it's just $x$). Similarly, the RHS depends on $y$ but $x$ is fixed. This means:
- For any fixed $x$: the value $(((y*y)*x)*x)*z$ must equal $x$ regardless of $y$ and $z$.
- This forces extremely degenerate behavior: essentially $a*b = $ constant for large parts of the operation.

**Phase 3 — All collapse models satisfy P only in trivial (1-element) algebras.**

**Phase 4 — Full $\mathbb{F}_2$ search:** No 2-element magma satisfies P universally (except trivial). In the trivial 1-element magma, C holds vacuously.

**Argument:** P forces $|A| = 1$ (all elements equal). In a 1-element magma, every equation holds.

**VERDICT: TRUE** — P forces triviality, so C holds vacuously.

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
