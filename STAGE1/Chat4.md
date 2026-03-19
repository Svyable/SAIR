# UNIVERSAL ALGEBRA SOLVER — COMPACT REFERENCE

## SYNTAX

$$t ::= x_i \mid (t \ast t)$$

$$P = \{t_i = u_i\},\quad C: (\alpha = \beta)$$

---

## SEMANTICS

$$\ast = \text{ arbitrary binary op}$$

$$\neg\text{Assoc},\ \neg\text{Comm},\ \neg\text{Cancel},\ \neg\text{Idemp}$$

unless explicitly in $P$

---

## LEGAL MOVES (ONLY)

| Rule | Statement |
|------|-----------|
| `REF` | $t = t$ |
| `SYM` | $t = u \Rightarrow u = t$ |
| `TRN` | $t = u,\ u = v \Rightarrow t = v$ |
| `CL`  | $t = u \Rightarrow (t \ast s) = (u \ast s)$ |
| `CR`  | $t = u \Rightarrow (s \ast t) = (s \ast u)$ |

No other rewrites allowed.

---

## FEATURE MAP

$$L(t) = \text{leftmost var},\qquad R(t) = \text{rightmost var}$$

$$M(t) = \text{parity vector over } \mathbb{F}_2$$

$$V(t) = \text{variables in } t$$

---

## COLLAPSE MODELS

| Model | Definition | Reduction |
|-------|-----------|-----------|
| $\mathsf{LP}$ | $a \ast b = a$ | $t \mapsto L(t)$ |
| $\mathsf{RP}$ | $a \ast b = b$ | $t \mapsto R(t)$ |
| $\mathsf{XOR}$ | $a \ast b = a \oplus b$ | $t \mapsto \bigoplus \text{ leaves}$ |
| $\mathsf{AND}$ | $a \ast b = a \land b$ | |
| $\mathsf{OR}$ | $a \ast b = a \lor b$ | |
| $\mathsf{K0}$ | $a \ast b = 0$ | |
| $\mathsf{K1}$ | $a \ast b = 1$ | |

$$\mathbb{F}_2 = \text{all } 16 \text{ ops on } \{0,1\}$$

---

## SOLVER

### `SOLVE(P ⇒ C):`

**STEP 0 — TRIVIAL TRUE**

$$C \in P \quad \text{or rename/substitution instance} \Rightarrow \mathbf{TRUE}$$

**STEP 1 — FAST SIGNAL**

$$V(C) \not\subseteq V(P) \Rightarrow \text{go directly to } \mathsf{LP}, \mathsf{RP}$$

**STEP 2 — COLLAPSE LOOP**

For each model in order: $\mathsf{LP} \to \mathsf{RP} \to \mathsf{XOR} \to \mathsf{AND} \to \mathsf{OR} \to \mathsf{K0} \to \mathsf{K1}$

do: reduce all terms

$$\text{if } (\exists \nu)\ P(\nu) = \text{true} \land C(\nu) = \text{false} \Rightarrow \mathbf{FALSE}$$

**STEP 3 — COMPLETE SEARCH**

$$\forall f \in \mathbb{F}_2:$$

$$\text{if } (\forall \nu)\ P(\nu) = \text{true} \text{ and } (\exists \nu)\ C(\nu) = \text{false} \Rightarrow \mathbf{FALSE}$$

**STEP 4 — PROOF**

Attempt derivation using only: `REF`, `SYM`, `TRN`, `CL`, `CR`

$$P \vdash C \Rightarrow \mathbf{TRUE}$$

**STEP 5**

$$\text{else: continue search (no guessing)}$$

---

## WITNESS FORMAT

$$A = \{0,1\},\ \ast = f,\ \nu: \text{assignment}$$

$$P(\nu) = \text{true},\qquad C(\nu) = \text{false}$$

---

## HARD RULES

- Never replace $x \ast x \to x$ unless proven
- Never reassociate: $(a \ast b) \ast c \neq a \ast (b \ast c)$
- Never commute: $a \ast b \neq b \ast a$
- Every rewrite must match `REF`/`SYM`/`TRN`/`CL`/`CR`

---

## META

$$\text{Proof = global constraint}$$

$$\text{Counterexample = single witness}$$

$$\Rightarrow \text{always try witness first}$$

$$\boxed{\textbf{CORE: } \exists f, \nu:\ P(\nu) \land \neg C(\nu) \Rightarrow \mathbf{FALSE}}$$

$$\boxed{\textbf{TRUE only if explicitly derived}}$$
