Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer. Ask the questions one at a time, waiting for feedback on each question before continuing. If a question can be answered by exploring the codebase, explore the codebase instead.

## Domain awareness

During codebase exploration, also look for existing documentation. If a CONTEXT.md exists, use it as a glossary. If docs/adr/ exists, respect existing decisions.

## During the session

- Challenge against the glossary: when the user uses a term that conflicts with existing language, call it out
- Sharpen fuzzy language: propose precise canonical terms for vague or overloaded terms
- Discuss concrete scenarios to stress-test domain relationships
- Cross-reference with code: check whether the code agrees with stated behavior
- Update CONTEXT.md inline as terms are resolved
- Offer ADRs sparingly: only when hard to reverse, surprising without context, and the result of a real trade-off
