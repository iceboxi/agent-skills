# Spec Fidelity Review

Use this branch when the review subject is an implementation spec produced from an accepted Design Doc or other accepted architecture baseline.

This is the same independent review authority as the main review skill, applied to a different artifact. Do not create a second review workflow.

## Inputs

- implementation spec;
- accepted Design Doc / confirmed decisions;
- prior design-review acceptance basis and reopen conditions;
- repository evidence only where it affects fidelity.

## Check

1. **Decision fidelity**
   - accepted ownership, interfaces, lifecycle, migration, ordering, negative requirements, and compatibility constraints are preserved;
   - implementation examples have not been promoted into required architecture;
   - unresolved recommendations have not become confirmed decisions.

2. **Testing decisions**
   - agreed seams still observe the intended behavior;
   - characterization / regression strategy can detect semantic drift;
   - device / hardware / OS validation is not misrepresented as unit coverage;
   - planned validation is not presented as completed evidence.

3. **Acceptance and reopen conditions**
   - acceptance criteria are observable;
   - migration / compatibility success criteria are concrete;
   - implementation evidence that must reopen design is explicit.

4. **Traceability**
   - architecture-relevant spec statements trace to accepted design, confirmed decisions, prototype evidence, ADR/wayfinder resolution, or current repository fact.

## Verdict

Use the same verdicts as the main review skill:

- ACCEPT
- ACCEPT WITH NON-BLOCKING NOTES
- REVISE
- BLOCKED

A finding that requires a new architecture decision returns to design. A fidelity/wording omission returns to to-spec or direct spec correction.

## When to use

Run this mode when the implementation spec will become a durable handoff for multi-session / multi-agent work, or when architecture fidelity is high-risk. Small single-context work does not require a second mandatory review ceremony.
