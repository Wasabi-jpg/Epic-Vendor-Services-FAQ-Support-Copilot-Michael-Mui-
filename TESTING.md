## Highlight how I simulate user flow via scenarios (Intagibility)

- Test question found on FAQ -> Goal should be to get that entry
- Test asking for password -> Goal should be to raise guardrails
- Test empty queries -> UI Doesn't allow for empty queries to be sent
- Test memory used

- Highlight scenarios, failsafe/safeguards, regressions (High Level Approach on how I build)
- Highlight how I thought about using Cursor during development relative to product




## Add Test Suite (Project Test Suite) (fully fleshed out)
check tests folder

## Highlighting AI prompting 
- Cursor wasn't as powerful as expected, although it definitely has good capabilities when
thoughts and plans are given to it first.
- First approach, brittle query word matching for ruleset, for the sake of less content given to model to reason an answer from.
- Cursor gave some ideas which led to new approach, of bigger model (llama3.1:8b) to fit all of the seed data with users query.
- Under new and bigger model approach, accuracy in my opinion (relevancy went up).
- Testing questions on FAQ: very precise.
- Testing asking for password, didn't make up steps.
- Testing empty queries -> UI still prevents empty queries
- Testing memory, still seems to have false positives of drawing from past conversation interactions, especially for
irrelevant topics (pricing to passwords)
