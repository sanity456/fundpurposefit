# Architecture

Project: PurposeCapLedger

Reusable primitive: semantic line-to-purpose mapping -> deterministic vector aggregation and cap test -> reviewer authorization.

The contract separates caller-attested public inputs, validator-agreed semantic fields, deterministic state transitions, and role-bound final actions. It stores canonical JSON strings in GenVM maps, validates every identifier and bound before consensus, and keeps source references explicitly unverified.

The mechanism is not a renamed assessment record. Its state transitions, role topology, storage layout, deterministic algorithm, and public ABI are specific to this project.

<!-- correction-release-start -->
## Consensus and storage safety boundary

The validator now canonicalizes the leader's attached expense-to-purpose mapping, derives the purpose mask and mapping digest from it, compares the full payload independently, and rebinds it after consensus before cap state is written.

The on-chain state transition consumes only the canonical value returned by the post-consensus binding boundary. This contract does not expose a shared permissionless fixed-cap operational registry.
<!-- correction-release-end -->
