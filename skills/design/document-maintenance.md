# Document Maintenance Mode

Use this branch only when the user asks to update an existing Design Doc with decisions that are already accepted.

This is not a new design pass.

## Authority

Use, in order:

1. explicit user-confirmed decisions;
2. accepted review findings / resolutions;
3. completed prototype / characterization / decision results;
4. the existing canonical Design Doc;
5. repository checks only when a referenced current-state claim is stale or contradictory.

## Rules

- Do not invent a new owner, protocol, API, runtime semantic, migration strategy, phase, or estimate.
- Do not silently promote examples or helper shapes into architecture contracts.
- Preserve existing terminology and document structure unless the accepted decision requires a change.
- Update all affected sections consistently: overview, diagrams, interfaces, flows, migration, estimates, and verification when applicable.
- If applying the accepted decision requires a new architecture choice, stop and return to normal design mode.

## Completion criterion

The canonical Design Doc faithfully reflects the accepted decisions, with no new design introduced by the synchronization itself.
