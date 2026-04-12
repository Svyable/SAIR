# SAIR Contest Cheat Sheet v2 (10x Performance + Robustness)

> Purpose: decide whether `E₁ ⊨ E₂` for one binary operation `*`.
> 
> Input:
> - `E₁ := {{ equation1 }}` (axiom schema you may instantiate)
> - `E₂ := {{ equation2 }}` (goal equation)

---

## 0) One-screen decision recipe

```text
parse -> normalize -> instant checks -> invariant gate -> M2 -> M3 -> proof search -> emit
```

Hard policy:

1. Return **FALSE** immediately on first valid finite counterexample.
2. Return **TRUE** only with a fully checked derivation chain using allowed rules.
3. Never assume hidden algebraic laws (assoc/comm/idemp/etc.) unless derivable from `E₁`.

---

## 1) Formal core

- Structure: `𝔐 = ⟨A,*⟩`, `A ≠ ∅`
- Terms: `τ ::= x | *(τ,τ)`
- Equation form: `u=v`

### 1.1 Do-not-assume law names

- `α`: associativity
- `χ`: commutativity
- `ι`: idempotence
- `κ`: cancellation
- `ε`: unit
- `ζ`: zero

Treat these as **false by default** unless proved from `E₁`.

### 1.2 Allowed derivation rules (`ρ`) only

- `r`: `t=t`
- `s`: `t=u ⇒ u=t`
- `t`: `t=u ∧ u=v ⇒ t=v`
- `l`: `t=u ⇒ *(t,w)=*(u,w)`
- `q`: `t=u ⇒ *(w,t)=*(w,u)`
- `σ`: instantiate `E₁` via variable→term substitution
- `c`: equal-substitution in identical context

Forbidden in final proof (`β`):

- `!rebracket`, `!swap`, `!xx>x`, `!cancel`, `!drop`, `!insert`, `!compare-eq`, `!hidden-laws`

---

## 2) 10x architecture (phases `κ₀..κ₉`)

- `κ₀` Parse to typed AST + variable inventory
- `κ₁` Hash-cons terms (DAG) + canonical serialization
- `κ₂` O(1)/O(n) trivial accept checks
- `κ₃` Invariant and impossibility probes
- `κ₄` Compile terms to stack programs / bytecode
- `κ₅` M₂ exhaustive op search (16 tables), SIMD-friendly valuation loop
- `κ₆` M₃ curated + beam expansion op search
- `κ₇` Proof search (bidirectional + meet-in-the-middle)
- `κ₈` Certificate verifier (independent checker)
- `κ₉` Emit strict output contract

Stop condition: first valid certificate (`FALSE` witness or `TRUE` derivation).

---

## 3) Data model that makes it fast

## 3.1 AST + DAG nodes

Each node stores:

- `id` (dense int)
- `kind` (`VAR` or `APP`)
- `left_id/right_id` (for `APP`)
- `hash` (64-bit structural hash)
- `size`, `height`, `var_mask`

Hash-cons rule:

- reuse existing node if `(kind,left,right,var)` matches
- gives pointer equality for exact tree equality

## 3.2 Bit-level variable representation

- Map each variable to bit position `0..63`.
- `var_mask(term)` enables instant subset tests and valuation indexing.

## 3.3 Bytecode evaluator

Compile each term once to reverse-polish instructions:

- `PUSH_VAR i`
- `APPLY_*`

Then evaluate for each valuation with fixed-size stack (array, no heap).

Why faster:

- no recursion
- no repeated AST traversal
- branch-predictable inner loop

---

## 4) Normalization and cheap wins

### 4.1 Canonicalization (`κ₁`)

- strip whitespace
- parse explicit binary structure only
- remove redundant enclosing parentheses
- alpha-rename for *comparison-only* signatures (never mutate proof terms)

### 4.2 Trivial TRUE checks (`κ₂`)

Return TRUE if any:

1. `lhs(E₂)` and `rhs(E₂)` are same DAG node
2. `E₂` is side-swap/alpha-rename equivalent of `E₁`
3. `E₂` is direct substitution instance `σ(E₁)`

### 4.3 Quick FALSE prefilters (`κ₃`)

Prefilters do **not** prove FALSE alone; they only prioritize model search:

- variable-set anomaly: `V(E₂) ⊄ V(E₁)`
- leaf constraints mismatch: leftmost/rightmost profile conflict
- shape-distance high (`tree_edit_proxy`)
- repetition profile mismatch (duplication pressure)

---

## 5) Counterexample engine (primary win path)

## 5.1 M₂ complete scan (guaranteed over 2-element magmas)

Domain `A={0,1}`. Operation table encoding `b00b01b10b11`.

Recommended order (fast practical hit-rate):

`[0011,0101,0000,1111,0001,0111,0110,1110,1000,1001,0010,0100,1011,1101,1010,1100]`

Per operation `f`:

1. Enumerate all valuations for vars in `E₁`; require `E₁` true for all.
2. If passed, enumerate valuations for vars in `E₂`; if one falsifies `E₂`, emit FALSE witness.

### 5.2 M₂ micro-optimizations

- Precompute valuation arrays by variable mask.
- Memoize `eval(term_id, valuation_id, op_id)`.
- Early abort universal checks on first failure.
- Evaluate `lhs` and `rhs` in same pass to reduce loads.
- Bitpack truth results for 64 valuations at once when possible.

## 5.3 M₃ robust scan (3-element magmas)

Domain `A={0,1,2}`.

Stage A (curated ops):

- `πL`, `πR`, constants, `min`, `max`, saturating add `min(x+y,2)`, handed asymmetric tables

Stage B (beam expansion):

- generate neighbors by flipping a few cells in promising tables
- rank by `E₁` satisfaction score then `E₂` violation potential

Stage C (optional exhaustive chunking):

- full 3-element space is `3^9 = 19683` operations
- split into deterministic chunks for parallel workers

### 5.4 Sound FALSE certificate

A FALSE output is valid iff you provide:

- explicit domain `A`
- full operation table
- valuation `μ`
- machine-checkable report: `∀ν E₁(ν)=true` and `E₂(μ)=false`

---

## 6) TRUE engine (derivation only, no heuristics leaked)

Goal: derive `lhs(E₂)=rhs(E₂)` via `ρ` only.

## 6.1 State graph

Node: equation term (or pair normalization state).
Edge: one justified step with label in `{σ,r,s,t,l,q,c}`.

## 6.2 Search strategy (fast + complete under bounds)

- bidirectional BFS from both endpoints
- iterative deepening on proof length
- meet-in-the-middle hash table by canonical term id
- prioritize frontier nodes by heuristic distance:
  - shape distance
  - variable multiset distance
  - context depth difference

## 6.3 Explosion controls

- substitution template caps by depth/size
- congruence expansion budget per level
- duplicate elimination using `(term_id, depth, provenance_signature)`

## 6.4 Sound TRUE certificate

Accept TRUE only after independent checker verifies each step:

- every edge rule-valid
- substitutions well-formed
- contexts identical where required
- chain ends exactly at `rhs(E₂)`

---

## 7) Correctness guardrails (non-negotiable)

- Parser rejects non-binary `*` arity.
- Variable names are lexical, never conflated by compare-only alpha-renaming.
- Model checker and proof checker are separate modules.
- No unchecked shortcut admitted into final proof output.
- Deterministic mode default: fixed seeds, fixed op ordering, fixed valuation ordering.

---

## 8) Performance blueprint (contest mode)

## 8.1 Time budget policy (example, adjust to judge limits)

- `κ₂ + κ₃`: 1–5 ms
- `κ₅ (M₂ exhaustive)`: 1–20 ms typical
- `κ₆ (M₃ curated+beam)`: 5–200 ms
- `κ₇ (proof)`: remaining budget with iterative deepening checkpoints

## 8.2 Parallel plan

- Worker 1: M₂ full
- Worker 2..N-1: M₃ chunks/beam
- Final worker: proof search
- Global atomic stop flag once any valid certificate is found

## 8.3 Caching plan

- L1: per-op valuation results
- L2: term bytecode outputs
- L3: proof frontier seen-set

Eviction policy: LRU by `(op_id, term_id)` pressure.

---

## 9) Strict I/O contract

```text
VERDICT: TRUE|FALSE
REASONING: compact trace of phases and key branch decisions
PROOF: non-empty iff VERDICT=TRUE
COUNTEREXAMPLE: non-empty iff VERDICT=FALSE
METRICS: ops_tested, valuations_checked, proof_nodes_expanded, wall_ms
```

### 9.1 FALSE witness format

```text
A={...}
operation_table:
  ...
μ: x↦..., y↦..., ...
E₁_universal: PASS
E₂_at_μ: lhs=..., rhs=... (lhs != rhs)
```

### 9.2 TRUE proof format

```text
1. term_0 = term_1   [rule: σ, details: ...]
2. term_1 = term_2   [rule: l, details: ...]
...
n. lhs(E₂) = rhs(E₂)
```

---

## 10) Pseudocode (reference implementation)

```text
function decide(E1, E2, budget_ms):
  ast1, ast2 = parse(E1), parse(E2)
  dag = hash_cons(ast1, ast2)
  if trivial_true(ast1, ast2, E1):
      return emit_true(trivial_certificate)

  probes = compute_probes(ast1, ast2)

  w = run_M2(ast1, ast2, probes)
  if w.valid:
      return emit_false(w)

  w = run_M3(ast1, ast2, probes, budget_slice)
  if w.valid:
      return emit_false(w)

  p = run_proof_search(ast1, ast2, E1, remaining_budget)
  if p.valid:
      return emit_true(p)

  return emit_unknown_as_continue_or_timeout()  // only if contest permits
```

If contest requires strict boolean only, continue search until one certificate is found.

---

## 11) Common failure modes + fixes

- **Bug:** accepted proof step used hidden commutativity.
  - **Fix:** checker rejects any unlabeled transform not in `ρ`.
- **Bug:** false counterexample because `E₁` not universally checked.
  - **Fix:** require complete valuation sweep over `vars(E₁)` before testing `E₂` witness.
- **Bug:** nondeterministic verdict across runs.
  - **Fix:** fixed ordering + seed + reproducible logs.
- **Bug:** proof search memory blow-up.
  - **Fix:** iterative deepening + frontier cap + disk spill optional.

---

## 12) Contest quick-start template

```text
E₁ = {{ equation1 }}
E₂ = {{ equation2 }}

run κ₀..κ₉ with deterministic mode = ON
return first valid certificate
```

Minimal deliverable:

- If FALSE: one valid finite witness.
- If TRUE: one fully labeled derivation chain.

No guessing. No hidden laws. Certificates only.
