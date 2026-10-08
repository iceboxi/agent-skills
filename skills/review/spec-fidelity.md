# Spec Fidelity Review

Use only on explicit user request to assess spec fidelity to confirmed decisions, requirements, ADRs, or an accepted prior architecture baseline. A post-spec standalone Design Doc does not automatically become implementation authority.

This is an optional mode of the same independent review skill, not another mandatory phase.

## Inputs

- implementation spec;
- confirmed decisions / requirements / ADRs (accepted prior design baseline only if one actually exists);
- prior review acceptance basis and reopen conditions, if available;
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

Use only when the user explicitly requests a fidelity review, for example with high-risk multi-session work. Do not run automatically after spec, tickets or Design Doc.
