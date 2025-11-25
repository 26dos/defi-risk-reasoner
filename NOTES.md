# notes


## caching

verified: cache hit ratio is ~70% on a 5-iteration agent run. saves real money.

## models

4.5 was fine for the analyst persona. 4.6 has slightly more tool-use willingness.

## eoy 2024

basic agent is working end to end. eval set up next.

## stress scenarios

the -50% eth move + +5% stablecoin pair is the one i actually care about most.

## tool result

we stringify tool outputs. this is fine but model sometimes infers types wrong from string. consider structured outputs later.

## paper

working title. won't submit anywhere serious until eval set is bigger (target n=200).

## ci

DON'T put real ANTHROPIC_API_KEY in actions. dummy key works for unit tests; integration tests run locally only.

## usage

added per-run token totals. cache_read_input_tokens is the line to watch.

## model bumps

plan: stay on 4.5 until 4.6 quality is verified on the full eval set.

## tools

current toolset is aave + chainlink + snapshot + morpho. should add: spark, gearbox, fluid.
