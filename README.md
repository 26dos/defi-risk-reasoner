# defi-risk-reasoner

Official reference implementation of "Tool-Using LLM Agents for DeFi
Position Risk Analysis" (working paper, 2025).

[Paper (preprint)](docs/PREPRINT.md) | [Demo transcripts](docs/transcripts/)

## Abstract

We present a Claude-based agent that ingests an Ethereum wallet address and
produces a structured risk report covering liquidation, oracle, and governance
exposure. The agent has access to a small set of on-chain read tools and is
constrained to cite its sources. We report on the agent's accuracy across a
hand-labeled set of 50 historical positions and show that the structured
output is comparable to a human analyst on the liquidation-distance task
while being faster and cheaper to produce at scale.

## Requirements

- Python 3.10+
- An Anthropic API key (`ANTHROPIC_API_KEY`)
- An Ethereum mainnet RPC (`ETH_RPC_URL`) — Alchemy / Infura / your own node
  all work

## Reproducing the agent runs

```bash
pip install -e .

cp .env.example .env  # then fill in keys

risk-reasoner analyze 0x73af3bcf944a6559933396c1577b257e2054d935 \
    --out reports/example.md
```

The first run will take 30-90 seconds depending on how many tool calls the
agent decides to make.

## Reproducing paper results

The labeled position set lives in `eval/positions.jsonl`. Each entry has a
wallet address and a hand-graded analysis. To run the agent over the set:

```bash
python eval/run_eval.py --out runs/$(date +%Y-%m-%d).jsonl
python eval/score.py --runs runs/2025-04-15.jsonl --gold eval/positions.jsonl
```

Reported numbers from the paper used `claude-sonnet-4-5` with prompt caching
enabled. The cost per analysis was ~$0.05 in API credits.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Citation

If this work is useful to you:

```bibtex
@misc{tan2025defirisk,
  author = {Wei Han Tan},
  title  = {Tool-Using LLM Agents for DeFi Position Risk Analysis},
  year   = {2025},
  url    = {https://github.com/26dos/defi-risk-reasoner},
}
```
