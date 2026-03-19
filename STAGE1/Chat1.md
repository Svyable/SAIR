--HARD3 = 7/10

# UNIVERSAL ALGEBRA SOLVER — STRUCTURE FIRST

**Universe:** $(A, \ast)$ free magma unless axioms add relations

---

## I. TERM GEOMETRY

$$t ::= x \mid (t \ast t)$$

View each term as a rooted ordered binary tree.

**Invariants:**

$$|t| = \text{node count},\quad \text{Vars}(t),\quad L_\ell(t),\quad L_r(t)$$

**Evaluation collapse maps:**

$$t^{\pi_1} = L_\ell(t), \qquad t^{\pi_2} = L_r(t)$$

---

## II. EQUALITY DYNAMICS

$$\text{EqCl}(P) = \text{smallest congruence containing } P$$

$$u = v \Rightarrow C[u] \sim C[v]$$

Only motion allowed: substitution inside identical context.

No structural deformation:

$$\neg((a \ast b) \ast c \sim a \ast (b \ast c)),\quad \neg(a \ast b \sim b \ast a)$$

unless explicitly given.

---

## III. MODEL SPACE

$$\mathbb{F}_2 = \{f : \{0,1\}^2 \to \{0,1\}\},\quad |\mathbb{F}_2| = 16$$

Term induces function: $t \mapsto \llbracket t \rrbracket_f : A^V \to A$

**Decision reduction:**

$$P \models C \iff \forall f \in \mathbb{F}_2\ [(\forall a)\ P(a) \Rightarrow (\forall a)\ C(a)]$$

Practically: $\exists f, a:\ P(a) \land \neg C(a) \Rightarrow \mathbf{FALSE}$

---

## IV. COLLAPSE LAYERS (SEARCH ORDER)

**Layer 1: projections**

$$\pi_1:\ t \mapsto L_\ell(t),\qquad \pi_2:\ t \mapsto L_r(t)$$

**Layer 2: constants**

$$c_0, c_1:\ t \mapsto 0 \text{ or } 1$$

**Layer 3: boolean structure**

$$\land,\ \lor,\ \oplus,\ \neg(\land),\ \neg(\lor)$$

**Layer 4: full $\mathbb{F}_2$**

---

## V. FAILURE MODES (GEOMETRIC)

- $\text{Vars}(C) \not\subseteq \text{Vars}(P)$
- $\text{depth}(C) > \text{depth}(P)$
- Tree mismatch: different branching patterns
- New subtrees in $C$ not present in $P$
- Symmetry mismatch: $P$ invariant, $C$ not

These correspond to directions in term space not constrained by $P$.

---

## VI. DUAL FORCES

- **Derivation:** $P \vdash C$ (within $\text{EqCl}$)
- **Refutation:** $\exists f, a:\ P(a) \land \neg C(a)$

**Asymmetry:**
- Derivation requires global structure
- Refutation requires single witness

$$\Rightarrow \text{optimize for refutation}$$

---

## VII. DECISION FLOW

$$C \in \text{EqCl}(P) \Rightarrow \mathbf{TRUE}$$

$$\exists f \in \mathbb{F}_2,\ a:\ P(a) \land \neg C(a) \Rightarrow \mathbf{FALSE}$$

Otherwise attempt explicit derivation.

---

## VIII. CORE PRINCIPLE

- Term algebra is high-dimensional tree space
- $P$ constrains a thin subset
- $C$ must lie in same constraint manifold
- Else a small projection of the space separates them

---

## IX. OUTPUT FORM

$$P: \ldots,\quad C: \ldots$$

$$P \vdash C \Rightarrow \mathbf{TRUE}$$

or

$$\exists (f, a):\ P(a),\ \neg C(a) \Rightarrow \mathbf{FALSE}$$

---

## X. META-INVARIANT

> No counterexample found + no derivation = continue search, not guess
