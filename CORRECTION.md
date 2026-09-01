# Correction and release record

Repository: fundpurposefit

Contract: PurposeCapLedger

Corrected release verified: 2026-09-01T09:13:17.233168Z

## Findings applied

This repository was checked against both steward findings from the rejected Boxcomplete and Baggate submissions:

1. A leader-provided digest is not proof of its attached substantive payload. Every result that affects state must be canonicalized, independently compared, and rebound after consensus.
2. A shared permissionless registry with fixed global capacity can be captured or exhausted. Operational catalogs must be explicitly owner-scoped, bounded per catalog, or safely reclaimable.
3. Corrected repository source is insufficient when the submitted Studio/Explorer address still runs an earlier build. The active address, deployed source, ABI, transaction, and evidence URLs must identify one release.

## Contract-specific correction

The validator now canonicalizes the leader's attached expense-to-purpose mapping, derives the purpose mask and mapping digest from it, compares the full payload independently, and rebinds it after consensus before cap state is written.

## Verified release lock

Current StudioNet address: 0x215FBa27157f5367e73225F782d4c599A0583B7c

Deployment transaction: 0x4bcc3938a081961a48ecdefe092ee2db0530249ca77f054f5fe9404a6f076ac3

Source SHA-256: ff23bddbd988ec92480585bd4e3966b98adc25f044230bd01d822bcade5f816b

Superseded address: 0x04791BbC23034F45531194D4d5cb2180a6343664

The deployment manifest records exact byte-for-byte source readback, exact full ABI/schema equality, successful finalized execution for all 5 release transactions, role-separated external wallets, and the final state observed from StudioNet. The superseded address is historical only and must not be used in a new submission.

## Regression evidence

GenVM lint and strict typecheck: pass

Direct tests: 11 pass

Five-validator integration tests: 1 pass

Leader-payload or post-consensus injection regression tests: pass

Registry isolation and reclaim tests: not applicable

## Review boundary

No web collection. Restriction text, categories, caps, expenses, and source references are frozen public caller declarations.

It does not move funds, authenticate restrictions, approve payment, or provide tax, accounting, fiduciary, or legal advice.

This record documents the implemented controls and verified release. It does not promise a particular human review outcome.
