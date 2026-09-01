# Submission checklist

- [x] Exactly one deployable contract source and one generated ABI
- [x] Concrete GenVM runner hash on line 1
- [x] GenVM lint and strict typecheck pass
- [x] Direct regression tests pass, including forged leader-result checks
- [x] Five-validator GLSim integration flow passes
- [x] Substantive payload is rebound to all derived hashes, masks, and state fields
- [x] Consensus output is canonicalized again before state mutation
- [x] Permissionless fixed-cap registries are absent or isolated and safely reclaimable
- [x] Source and provenance boundaries are explicit and accurate
- [x] No wallet secrets or private key material are stored in the repository
- [x] Fresh repository-specific external StudioNet wallets were used
- [x] Every recorded StudioNet transaction finalized and executed successfully
- [x] Deployed source matches the corrected repository source byte-for-byte
- [x] Full deployed schema matches abi.json exactly
- [x] Active Studio, Explorer, transaction, and manifest evidence use `0x215FBa27157f5367e73225F782d4c599A0583B7c`
- [x] Superseded address `0x04791BbC23034F45531194D4d5cb2180a6343664` is excluded from active submission evidence
- [x] Submission evidence is pinned to corrected release commit `0c6d66a769643be075ab75fe138dbc48e0da5028`
