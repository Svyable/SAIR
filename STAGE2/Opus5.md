## ADVERSARIAL SELF-CHECK MAGMA SOLVER

You must solve this problem THREE times using different methods. If all three agree, output that answer. If they disagree, find your error.

---

### METHOD 1: BRUTE FORCE TRUTH TABLE

Enumerate. Do not think. Just compute.

**Step 1.** Write down Equation 1 (Premise P) and Equation 2 (Conclusion C).

**Step 2.** List variables: $V_P$, $V_C$, $V_{\text{new}} = V_C \setminus V_P$.

**Step 3.** For each of the 16 binary operations on $\{0,1\}$, encoded as 4-bit vector $(f_{00}, f_{01}, f_{10}, f_{11})$:

**Step 3a.** Build evaluation table for P. For every $\nu \in \{0,1\}^{|V_P|}$:
- Compute LHS(P) step by step (show each subterm)
- Compute RHS(P) step by step
- Record: MATCH or MISMATCH

If ANY row is MISMATCH: this operation does not satisfy P. Skip to next operation.

**Step 3b.** If all rows MATCH (P is universally satisfied): build evaluation table for C. For every $\mu \in \{0,1\}^{|V_C|}$:
- Compute LHS(C) step by step
- Compute RHS(C) step by step
- Record: MATCH or MISMATCH

If ANY row is MISMATCH: **COUNTEREXAMPLE FOUND.** Record $(f, \mu)$.

**Step 4.** Tally results.

---

### METHOD 2: STRUCTURAL ANALYSIS

**Step 1. Variable flow analysis:**
- Draw the term tree for each side of P and each side of C
- Track where each variable appears (position, depth, left/right child)
- Compare: does C require a variable to "move" to a position not reachable from P?

**Step 2. Invariant checking:**
For each of these invariants, check if P preserves it but C violates it:

| Invariant | Description | Failure means |
|-----------|-------------|---------------|
| Leftmost variable | $L(\text{LHS}) = L(\text{RHS})$ | FALSE via LP model |
| Rightmost variable | $R(\text{LHS}) = R(\text{RHS})$ | FALSE via RP model |
| Leaf parity | $\bigoplus \text{leaves(LHS)} = \bigoplus \text{leaves(RHS)}$ | FALSE via XOR model |
| Variable set | $\text{Var(LHS)} = \text{Var(RHS)}$ | Investigate further |
| Depth balance | Relative depths of shared subterms | May indicate structural impossibility |

**Step 3. Substitution space analysis:**
- What substitution instances of P are available?
- Can they produce the subterms needed for C?
- Is there a "gap" — a subterm in C that cannot be generated from P?

---

### METHOD 3: MODEL-THEORETIC REASONING

**Step 1. Classify the premise:**
What does P force? Analyze which operations satisfy P.

| Category | Operations satisfying P | Implication |
|----------|----------------------|-------------|
| Only trivial (constant/projection) | Forces degenerate algebra | Likely TRUE (vacuously) |
| Multiple non-trivial | Rich model space | Counterexample likely exists |
| None on $\{0,1\}$ | May force $|A| = 1$ | TRUE if $|A|=1$ forced |

**Step 2. If P forces triviality:**
- Check: does P hold in the 1-element magma? (Always yes.)
- If P forces $|A| = 1$, then C holds vacuously → TRUE.
- Verify by checking: does P hold in ANY 2-element magma? If no → P forces $|A| = 1$.

**Step 3. If P has non-trivial models:**
- For each model of P, can we find a C-violating assignment?
- The more free variables C has (especially new ones not in P), the easier this is.
- Try: take a non-trivial model of P, set variables in $V_P$ to satisfy P, then vary $V_{\text{new}}$.

---

### CONVERGENCE CHECK

```
Method 1 says: ______
Method 2 says: ______
Method 3 says: ______
```

**If all three agree:** High confidence. Output that verdict.

**If Methods disagree:**
- The BRUTE FORCE method (Method 1) is the most reliable — trust it over the others.
- Re-examine the disagreeing method for errors.
- Common errors:
  - Evaluation mistake (mis-applying the operation table)
  - Structural analysis overlooked a valid derivation path
  - Model-theoretic reasoning missed a model or dismissed a vacuous case

---

### PRE-SOLVE PATTERN RECOGNITION

Before starting, check these fast patterns:

**Pattern F1 (New free variable, non-trivial P):**
$V_C \supsetneq V_P$ AND $\exists$ non-trivial 2-element model of P
→ Almost certainly **FALSE** (new variable can break C)

**Pattern F2 (Structure mismatch):**
Under LP: $L(\text{LHS}(C)) \neq L(\text{RHS}(C))$ AND LP satisfies P
→ Definitely **FALSE**

**Pattern T1 (Trivial forcing):**
No 2-element magma satisfies P → P forces $|A|=1$ → **TRUE**

**Pattern T2 (Same equation):**
C is a substitution instance of P (or vice versa) → **TRUE**

**Pattern T3 (P is very strong):**
P equates terms of very different structure → P heavily constrains $*$ → likely TRUE

---

### DOUBLE-CHECK EVAL PROCEDURE

When computing $\text{eval}(t, f, \nu)$, use this explicit format:

```
Term: x * (y * z)
Assignment: x=0, y=1, z=0
Operation: f(0,0)=1, f(0,1)=0, f(1,0)=1, f(1,1)=0

  y * z  =  f(1, 0)  =  1
  x * (y*z)  =  f(0, 1)  =  0

Result: 0
```

**Show EVERY intermediate computation.** Errors hide in skipped steps.

---

### ABSOLUTE RULES

1. **Three methods, one answer.** Do not output until methods converge.
2. **Show your work.** Every evaluation, every proof step.
3. **No hidden assumptions.** The operation $*$ has NO properties unless forced by P.
4. **Counterexample beats conjecture.** One verified counterexample overrides any amount of "it seems like it should be true."
5. **Proof beats intuition.** A step-by-step derivation overrides "it seems false."
6. **When in doubt, enumerate.** There are only 16 operations × at most 32 assignments. You can check them all.

---

### OUTPUT TEMPLATE

```
=== METHOD 1 (Brute Force) ===
Operations satisfying P: [list IDs]
For each, C holds? [yes/no, with counterexample if no]
Method 1 verdict: [TRUE/FALSE]

=== METHOD 2 (Structural) ===
Variable analysis: [findings]
Invariant checks: [findings]
Method 2 verdict: [TRUE/FALSE]

=== METHOD 3 (Model-Theoretic) ===
P classification: [trivial-forcing / rich models / ...]
Model analysis: [findings]
Method 3 verdict: [TRUE/FALSE]

=== CONVERGENCE ===
All methods agree: [YES/NO]
[If NO: resolution of disagreement]

VERDICT: [TRUE/FALSE]
REASONING: [from converged analysis]
PROOF: [if TRUE]
COUNTEREXAMPLE: [if FALSE]
```
