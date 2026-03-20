## ALGORITHMIC MAGMA SOLVER — PYTHON-IN-YOUR-HEAD

Execute this algorithm mentally. Do NOT skip steps. Do NOT guess.

---

### STEP 0: PARSE

Write both equations in explicit binary-tree notation:
- Every `*` takes exactly two arguments
- Use parentheses to show exact tree structure
- List: $V_P$ = variables in P, $V_C$ = variables in C, $V_{new} = V_C \setminus V_P$

---

### STEP 1: ENUMERATE $\mathbb{F}_2$

All 16 binary operations on $\{0,1\}$ encoded as $(f(0,0), f(0,1), f(1,0), f(1,1))$:

```
 ID | f(0,0) f(0,1) f(1,0) f(1,1) | Name
----|-------------------------------|------
  0 |   0      0      0      0     | ZERO
  1 |   0      0      0      1     | AND
  2 |   0      0      1      0     | x>y (x AND NOT y)
  3 |   0      0      1      1     | PROJ_L (π₁)
  4 |   0      1      0      0     | y>x (y AND NOT x)
  5 |   0      1      0      1     | PROJ_R (π₂)
  6 |   0      1      1      0     | XOR
  7 |   0      1      1      1     | OR
  8 |   1      0      0      0     | NOR
  9 |   1      0      0      1     | XNOR
 10 |   1      0      1      0     | NOT_R
 11 |   1      0      1      1     | x OR NOT y
 12 |   1      1      0      0     | NOT_L
 13 |   1      1      0      1     | y OR NOT x
 14 |   1      1      1      0     | NAND
 15 |   1      1      1      1     | ONE
```

---

### STEP 2: EVALUATE

For each operation $f$ (ID 0–15):

**2a.** Compute P on all assignments $\nu : V_P \to \{0,1\}$.
- Evaluate LHS(P) under $f$ and $\nu$
- Evaluate RHS(P) under $f$ and $\nu$
- P *holds under $f$* iff LHS = RHS for ALL $\nu$

**2b.** If P holds under $f$: compute C on all assignments $\mu : V_C \to \{0,1\}$.
- If $\exists \mu$ where LHS(C) $\neq$ RHS(C): **COUNTEREXAMPLE FOUND**
- Record: $f$, $\mu$, LHS value, RHS value

**Evaluation procedure for a term $t$ under operation $f$ and assignment $\nu$:**
```
eval(x_i, f, ν) = ν(x_i)
eval((s * t), f, ν) = f(eval(s, f, ν), eval(t, f, ν))
```

Work inside-out, from leaves to root.

---

### STEP 3: DECIDE

**If counterexample found in Step 2:**
```
VERDICT: FALSE
COUNTEREXAMPLE:
  A = {0, 1}
  Operation: f(0,0)=_, f(0,1)=_, f(1,0)=_, f(1,1)=_
  Assignment: x=_, y=_, z=_, ...
  LHS(C) evaluates to _
  RHS(C) evaluates to _
  All premises satisfied: [verify each]
```

**If NO counterexample in any of 16 operations:**
Proceed to Step 4 (derivation attempt).

---

### STEP 4: DERIVE (only if Step 3 found no counterexample)

Attempt proof using the 5 legal rules. Strategy:

**4a. Substitution mining:** List useful instances of P by choosing specific substitutions:
- $\sigma_1 = \{x \mapsto x, y \mapsto y, z \mapsto z\}$ (identity — P itself)
- $\sigma_2 = \{x \mapsto \text{LHS}(P), \ldots\}$ (substitute P's LHS into P)
- $\sigma_3$: match subterms of C to find what substitution would produce them

**4b. Build chain:** Start from LHS(C), apply substitution instances + congruence rules to reach RHS(C).

**4c. Verify:** Every single step must be justified by exactly one rule.

```
VERDICT: TRUE
PROOF:
  Step 1: [equation] by [rule] with [details]
  Step 2: [equation] by [rule] with [details]
  ...
  Final: LHS(C) = RHS(C)
```

---

### STEP 5: PRIORITY ORDER FOR REFUTATION

When testing operations, prioritize in this order (most likely to find counterexamples first):

1. **PROJ_L (ID 3):** $a*b = a$. Kills all right arguments.
2. **PROJ_R (ID 5):** $a*b = b$. Kills all left arguments.
3. **XOR (ID 6):** $a*b = a \oplus b$. Tests linearity/parity.
4. **AND (ID 1):** Tests monotone collapse downward.
5. **OR (ID 7):** Tests monotone collapse upward.
6. **ZERO (ID 0), ONE (ID 15):** Constant operations.
7. **Remaining 9 operations.**

For each operation where P holds, if $V_{new} \neq \emptyset$, the new variable is universally quantified in C — try setting it to both 0 and 1.

---

### CRITICAL VERIFICATION CHECKLIST

Before outputting your answer:

- [ ] Did I check ALL 16 operations? (Not just the 7 named ones)
- [ ] For each operation satisfying P, did I check ALL assignments for C?
- [ ] If FALSE: does my witness actually satisfy P? (Recompute P under my witness)
- [ ] If FALSE: does my witness actually violate C? (Recompute C under my witness)
- [ ] If TRUE: does every proof step use exactly one legal rule?
- [ ] If TRUE: did I verify the proof by replaying it end-to-end?
- [ ] Did I avoid assuming associativity, commutativity, idempotence, or cancellation?

---

### SELF-CORRECTION PROTOCOL

If you are uncertain:
1. Pick the 3 most likely counterexample operations
2. Fully evaluate P on all $2^{|V_P|}$ assignments for each
3. For those satisfying P, fully evaluate C on all $2^{|V_C|}$ assignments
4. Show your work explicitly with a truth table

**Never output TRUE without a complete derivation.**
**Never output FALSE without a verified counterexample.**
