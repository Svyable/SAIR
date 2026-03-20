# SAIR — Magma Equation Implication Competition

## Overview

This competition explores a core question in AI for mathematics: can strong mathematical reasoning be distilled into a compact, human-readable cheatsheet that improves LLM performance on formal tasks?

This competition is organized by:
- **Damek Davis** (Associate Professor, Department of Statistics and Data Science, University of Pennsylvania)
- **Terence Tao** (Fields Medalist, Professor at UCLA, Co-Founder of SAIR Foundation)
- and the **SAIR Foundation**

The setup is inspired by Honda, Murakami, and Zhang (2025), *Distilling Many-Shot In-Context Learning into a Cheat Sheet*. Our difference is that cheatsheets are discovered through an open competition process rather than a single model query.

---

## Background

The pilot task is **equational implication over magmas**: given Equation 1 and Equation 2, determine whether Equation 1 implies Equation 2.

This challenge is based on the **Equational Theories Project**.

> Example: E_4: `x = x * y` implies E_3: `x = x * x`.

- Raw implication graph: `export_raw_implications`
- Law list (4694 laws): `equations.txt`

---

## Core Task

Participants submit a **cheatsheet** (plain text prompt guidance). The model then solves implication problems of the form:

> Does Equation 1 imply Equation 2?

In Stage 1, the expected behavior is to provide a **true/false** answer to the question.

---

## Evaluation Format

### Stage 1 (Lower Barrier)

- **Task:** determine whether Equation 1 implies Equation 2.
- **Cheatsheet size cap:** 10KB.
- **Scoring focus:** correctness (right/wrong) only.

### Stage 2 (Higher Difficulty)

Harder benchmark setting than Stage 1. Participants may be required to submit one of:
- an explicit counterexample,
- an explicit Lean proof/disproof,
- or a calibrated confidence probability for implication truth.

Detailed rules: TBD.

---

## Key Dates

| Milestone | Date |
|-----------|------|
| Stage 1 starts | March 14, 15:09:26 (UTC+14), 2026 |
| Stage 1 submission deadline | April 20, 23:59 AoE, 2026 |
| Stage 1 leaderboard release | on or before April 30, 2026 |
| Stage 2 starts | May 1, 2026 |

---

## Stage 1 Training and Evaluation Rules

**Public selected problem subsets for Stage 1:**
- `normal`: 1000 normal-difficulty problems — Hugging Face: `normal`
- `hard1`: 69 hard-difficulty problems — Hugging Face: `hard1`
- `hard2`: 200 hard-difficulty problems — Hugging Face: `hard2`

Additional rules:
- Participants may also use additional problems from the Equational Theories Project for training.
- Stage 1 evaluation set is **balanced**: 50% TRUE implications and 50% FALSE implications.
- After submission deadline, organizer runs **offline evaluation**.
- Offline evaluation is conducted in a **no-tools setting**: the evaluation pipeline does not provide browser access, web search, or external internet retrieval to the models.
- Offline evaluation set is **different** from the 1269 public selected problems.
- We recommend an average cost of no more than **USD 0.01 per problem** and a solve time of no more than **10 minutes per problem**; exceeding time or budget limits may negatively affect final ranking.
- Top-performing teams in Stage 1 will advance to Stage 2, with no more than 1,000 teams in total.

---

## Evaluation Models

We expect to use lower-cost models for evaluation, including both open-source and proprietary models that are practical for large-scale benchmarking. Example candidates include OpenAI OSS models, Llama models, and Gemini Flash models. Since the model landscape may change during the competition, the final evaluation model list will be either announced by the organizers or determined through an organizer-initiated community vote, no later than **April 10, 2026**.

---

## Playground and Recommended Workflow

- A playground is provided to help participants test submissions and understand the competition workflow.
- The playground is designed to be usable even for participants with no AI development experience.
- For professional AI researchers, we recommend setting up your own environment with the recommended evaluation prompt to better participate in the competition and rigorously test cheatsheets.

---

## Publication Policy After Stage 1

- Stage 1 submitted cheatsheets may be made public to support community learning and strategy exchange.
- This is expected to remain fair because Stage 2 is substantially harder and allows larger cheatsheets, so Stage 1 winners are not guaranteed to transfer directly.

---

## Team Participation and Anti-Cheating Policy

- Each individual or organization can participate in only one team.
- Teams must register members and sponsors in advance.
- If coordinated cheating is detected (including sockpuppet teams), all related teams will be disqualified.

---

## Current Scope

This version of the competition implementation focuses on **Stage 1**.

---

## Experimental Status

This challenge is currently in an experimental phase. Rules, scoring details, and evaluation procedures may be adjusted based on implementation experience and community feedback.

Community contributions are welcome. Join the SAIR Foundation Zulip community for discussion and collaboration:
- https://zulip.sair.foundation/

---

## Repository Analysis

### Structure

```
SAIR/
├── STAGE1/          # Stage 1 cheatsheet submissions
│   ├── Chat1.md     # Structure-first universal algebra solver (scored 7/10 on HARD3)
│   └── Chat4.md     # Compact reference with collapse model table + step-by-step solver
└── STAGE2/          # Stage 2 cheatsheet development
    ├── Opus1.md     # Full decision cheatsheet with worked examples (most comprehensive)
    ├── Opus2.md     # Algorithmic "Python-in-your-head" solver with full F₂ enumeration table
    ├── Opus3.md     # (additional variant)
    ├── Opus4.md     # (additional variant)
    ├── Opus5.md     # Adversarial self-check solver — triple-method convergence approach
    └── tools/       # Python scripts for offline verification
        ├── magma_quick.py
        ├── magma_exhaust4.py
        ├── magma_size5_p0.py
        ├── magma_size5_p1.py
        ├── magma_prove.py
        ├── magma_algebraic.py
        ├── magma_derivations.py
        └── ... (18 scripts total)
```

### Cheatsheet Approach Summary

The cheatsheets in this repo all converge on a shared algorithmic framework for deciding magma equation implication:

#### Core Decision Algorithm

1. **Variable check** — if the conclusion C introduces new variables not in the premise P, flag as likely FALSE (free variables almost always admit counterexamples unless P forces a trivial algebra).
2. **Collapse model testing** — evaluate P and C over seven named models (LP, RP, XOR, AND, OR, K0, K1) on the 2-element set `{0,1}`. Any model satisfying P but violating C is an immediate FALSE counterexample.
3. **Full F₂ search** — enumerate all 16 binary operations on `{0,1}`. This is a complete procedure for 2-element algebras but is **not always sufficient** — some FALSE implications require size-5 magmas for a counterexample.
4. **Equational derivation** — if no counterexample is found, attempt a symbolic proof using only the five legal rules: REF, SYM, TRN, SUB, CL, CR.

#### Key Findings Encoded in Cheatsheets

- **Idempotence, associativity, and commutativity are NEVER assumed** unless explicitly forced by P.
- Some problems only have counterexamples in algebras of size 5 or larger; the `tools/` scripts provide Python implementations for size 3, 4, and 5 exhaustive search.
- The "adversarial self-check" approach (Opus5.md) runs three independent methods and requires convergence before committing to an answer — a strong guard against LLM hallucination errors.
- Cheatsheets are designed to be used in a **no-tools, offline** setting where the model must reason purely from the prompt guidance.

#### Python Tools (`STAGE2/tools/`)

The tools directory contains 18 Python scripts implementing offline algebraic verification:
- `magma_quick.py` / `magma_exhaust4.py` — fast F₂ and size-4 exhaustive search
- `magma_size5_p0.py` / `magma_size5_p1.py` — size-5 counterexample search for specific problem classes
- `magma_prove.py` / `magma_derivations.py` — automated equational derivation search
- `magma_algebraic.py` / `magma_smart.py` — higher-level algebraic reasoning utilities

These scripts serve as ground-truth validators for cheatsheet development and can be used to generate training examples or verify claimed counterexamples.
