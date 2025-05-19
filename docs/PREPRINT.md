# Tool-Using LLM Agents for DeFi Position Risk Analysis

*Preprint, last updated 2025-05.*

## 1. Introduction

DeFi positions are exposed to a small number of well-understood risks
(liquidation, oracle manipulation, governance attacks, smart contract bugs)
but the data needed to assess them is scattered across many on-chain calls
and off-chain APIs. Existing dashboards (DeBank, Zapper) surface position
state but do not produce risk *narratives*. Conversely, ChatGPT-style
analysts lack live data access.

We argue that a small, tool-using LLM agent is the right primitive for this
gap: it can pull live state, reason about it under a fixed analytical
schema, and produce a structured report. The contribution here is mostly
infrastructural — we describe a design, ship a reference implementation,
and report initial accuracy numbers.

## 2. System design

The agent is a vanilla Anthropic tool-use loop with four read-only tools:

  - `fetch_aave_v3_summary(user)` — aggregate Aave V3 state
  - `fetch_chainlink_feed(aggregator)` — latest answer + staleness
  - `stress_position(collateral, debt, liq_threshold)` — pre-baked scenarios
  - `fetch_governance_proposals(space_id)` — recent Snapshot proposals

The system prompt fixes the report structure (5 sections, see `prompts.py`)
and demands citations to tool calls.

## 3. Evaluation

We hand-graded 50 positions across August-November 2024 with a binary
"would-be-flagged-by-a-human-analyst" label per risk axis. Agent vs. human
F1:

  - Liquidation distance (within 5 percentage points): 0.93
  - Oracle staleness flag: 0.97
  - Governance flag (subjective): 0.71

The governance score is low because human raters disagree among themselves
(inter-rater κ = 0.42).

## 4. Limitations

  - Read-only tools only; we cannot test counterfactual mitigations.
  - Aave V3 only; expanding to other lending markets is straightforward but
    not done here.
  - Smart contract risk is not assessed — that requires either an LLM
    audit pass or static analysis integration.
