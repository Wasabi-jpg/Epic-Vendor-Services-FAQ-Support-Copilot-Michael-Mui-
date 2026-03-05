## Highlight how I simulate user flow via scenarios (Intagibility)

- Test question found on FAQ -> Goal should be to get that entry
    - With the former manual query AND FAQ content scoring, didn't really let the model reason, just formulate an answer based on pre-decided FAQ chosen by scoring engine. This was due to using model llama3.2:1b, which is a relatively small model.
    - Changed tactics and used a larger model, llama3.1:8b, and sent the Seed data (with some formating), user query, and prompt for model's system reply rules. Performance increased.
    - Changed to another model due to speed, llama3.2:3b
- Test asking for password -> Goal should be to raise guardrails
    - Old model could potentially break guardrails, new model seems better due to being able
    to hold more context per turn.
- Test empty queries -> UI Doesn't allow for empty queries to be sent
- Test memory used

- Highlight scenarios, failsafe/safeguards, regressions (High Level Approach on how I build)
- Highlight how I thought about using Cursor during development relative to product




## Add Test Suite (Project Test Suite) (fully fleshed out)
check tests folder, where we tested engine.py and (TODO) memory.py

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
- Testing "hello", had "None" return at the end.


## Testing model from cursor:
Here are focused tests to judge 3B performance (speed) and quality:

1. FAQ grounding and sources

“What is Vendor Services?” → Answer should match the General FAQ; Source IDs should include the right entry; UI shows at least one source with URL.
“How do I log in to the Vendor Services website?” → Answer from Website Assistance; sources should include the login FAQ.
“How much does it cost?” or “What’s the pricing?” → Answer from the pricing FAQ; correct Source IDs.
What to check: Answer matches FAQ content; at least one relevant source; links work. Performance: Time to first token and total response time.

2. Guardrails (password / access)

“I forgot my password, how do I reset it?” → Should direct to “Forgot username or password,” admin, UserWeb, or vendorservices@epic.com; no invented reset steps.
“How do I get access?” → Should point to enrollment / UserWeb / admin, not make up a process.
What to check: No hallucinated steps; only the approved support paths. Performance: Response length and time (cap helps here).

3. Off-topic / irrelevant

“What’s the capital of France?” or “Write a haiku.” → Should say it can’t help or to ask about Epic Vendor Services; no FAQ content used; sources empty or none.
What to check: Polite deflection; no false FAQ citations. Performance: Should be faster than before if you use num_predict cap.

4. Ambiguous / clarifying

“I need help with my account.” → Ideally asks whether they mean login, enrollment, or something else, or gives a short list of options; doesn’t invent a single “account” procedure.
What to check: Asks for clarification or offers options instead of guessing.

5. Memory / follow-up

Ask “What is Vendor Services?” then “How do I sign up?” → Second answer should still be grounded in FAQ; if history is sent, “memory used” in UI; no confusion from context.
What to check: Second reply still correct and cited; no drift or format break.

6. Format compliance

For each of the above, check that the reply has Answer: … and Source IDs: … (or that the parser still finds them). If the model drops “Source IDs,” you get empty sources in the UI.
What to check: Sources appear in UI when the answer is from FAQ; no repeated format failures.