# Design Doc Maintenance Mode

Use only when the user asks to refresh an **existing, self-contained Design Doc** after source decisions, implementation planning, or actual implementation facts have changed.

This is bounded documentation synchronization, **not** a new architecture design or implementation planning pass.

## Source authority

1. Latest explicitly confirmed requirements / architecture decisions and ADRs.
2. Current authoritative implementation spec / plan and resolved changes.
3. Verified implementation / characterization / prototype evidence.
4. Existing Design Doc as the previous **documentation snapshot**, not the implementation authority.
5. Repository evidence for current-state / implementation claims.

## Rules

- Update all impacted narrative, diagrams, interface sketches, runtime views, phases, estimates and validation claims consistently.
- Keep the Design Doc independently readable; do not replace missing explanation with links or references to upstream documents.
- Never expose issue / ticket IDs, titles, statuses, tracker links or ticket-to-phase mapping.
- Do not invent a new state owner, protocol, API, migration gate, implementation dependency, phase decision or estimate.
- Distinguish proposed design, newly verified implementation, and still-unresolved gaps.
- If sources require a fresh decision, hand it back to the owning requirement / spec / planning process instead of resolving it during synchronization.
- Do not demand document maintenance for every private helper change; refresh when the user needs an up-to-date human-facing document.

## Completion criterion

The standalone Design Doc faithfully reflects current confirmed source decisions and known implementation evidence, without introducing a competing implementation contract.
