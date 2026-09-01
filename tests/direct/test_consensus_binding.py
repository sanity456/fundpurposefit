"""Adversarial expense-mapping binding regressions."""

import hashlib
import json

from tests.direct.test_purpose_cap_ledger import _map, _program, _proposal


HONEST_ASSIGNMENTS = [{"expense_id": "E1", "category_id": "EDU"}]


def _hash(assignments):
    wire = json.dumps(assignments, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(wire.encode("ascii")).hexdigest()


FORGED = {"assignments": [{"expense_id": "E1", "category_id": "UNMAPPED"}], "mapping_sha256": _hash(HONEST_ASSIGNMENTS)}


def _captured(contract, vm, publisher, proposer, reviewer):
    program_id = _program(contract, vm, publisher, reviewer)
    proposal_id = _proposal(contract, vm, proposer, program_id)
    _map(contract, vm, proposer, proposal_id)
    return proposal_id


def test_validator_rejects_changed_mapping_with_honest_hash(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    _captured(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    assert direct_vm.run_validator(leader_result=FORGED) is False


def test_validator_accepts_honest_complete_mapping(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    _captured(contract, direct_vm, direct_alice, direct_bob, direct_charlie)
    assert direct_vm.run_validator() is True


def test_post_consensus_forgery_preserves_submitted_proposal(contract, direct_vm, direct_alice, direct_bob, direct_charlie, monkeypatch):
    from genlayer import gl

    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id)
    before = contract.get_proposal(proposal_id)
    direct_vm.sender = direct_bob
    monkeypatch.setattr(gl.vm, "run_nondet_unsafe", lambda *args: FORGED)
    with direct_vm.expect_revert("mapping_hash_mismatch"):
        contract.map_and_check(proposal_id)
    assert contract.get_proposal(proposal_id) == before
