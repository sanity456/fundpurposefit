# PurposeCapLedger

A reusable no-funds program ledger where validators map expense lines to purpose categories, code totals each category against its cap, and a designated reviewer acts only on within-cap proposals.

The repository is standalone and the contract is reusable: one deployment can hold multiple independent records for unrelated callers. It has no frontend and moves no funds.

## Native mechanism

semantic line-to-purpose mapping -> deterministic vector aggregation and cap test -> reviewer authorization.

## Actors

program publisher, proposer, designated reviewer, GenLayer validators.

## Source boundary

No web collection. Restriction text, categories, caps, expenses, and source references are frozen public caller declarations.

## Safety boundary

It does not move funds, authenticate restrictions, approve payment, or provide tax, accounting, fiduciary, or legal advice.

All inputs and results are public. Untrusted public data is delimited in prompts and cannot change the closed response schema. A malformed or non-consensus model result fails without committing the intended state transition.

## Verification

    genvm-lint check contracts/purpose_cap_ledger.py
    genvm-lint typecheck contracts/purpose_cap_ledger.py --strict
    python -m pytest tests/direct -q -p no:cacheprovider
    python tests/run_glsim.py --port 4000 --validators 5 --no-browser
    python -m pytest tests/integration -q -s -p no:cacheprovider

See ARCHITECTURE.md, SECURITY.md, SOURCE_PROVENANCE.md, AUDIT.md, SUBMISSION_CHECKLIST.md, and deployments/studionet.json.

MIT licensed.

<!-- correction-release-start -->
## Corrected release integrity

The full twelve-repository correction audit applied both steward findings to this contract. The validator now canonicalizes the leader's attached expense-to-purpose mapping, derives the purpose mask and mapping digest from it, compares the full payload independently, and rebinds it after consensus before cap state is written.

The current StudioNet release is `0x215FBa27157f5367e73225F782d4c599A0583B7c`. Its source bytes and full schema were read back from StudioNet and matched this repository exactly. Use `CORRECTION.md`, `REVIEW_RESPONSE.txt`, and the commit-pinned `deployments/studionet.json` for submission evidence; do not reuse the superseded address `0x04791BbC23034F45531194D4d5cb2180a6343664`.
<!-- correction-release-end -->
