"""Direct tests for category mapping and deterministic caps."""

import json


CATEGORIES = json.dumps({"categories": [
    {"id": "EDU", "purpose": "Direct community education materials and facilitated learning sessions.", "cap_units": 1000},
    {"id": "OPS", "purpose": "Documented operational supplies supporting the registered program.", "cap_units": 500},
]})
EXPENSES = json.dumps({"expenses": [{"id": "E1", "description": "Printed learning workbooks for the scheduled class.", "amount_units": 400}]})


def _program(contract, vm, publisher, reviewer):
    vm.sender = publisher
    return contract.publish_program("COMMUNITY", reviewer, CATEGORIES, "Funds may support only the two frozen public purpose categories and their stated caps.", "donor-restriction-snapshot")


def _proposal(contract, vm, proposer, program_id, expenses=EXPENSES):
    vm.sender = proposer
    return contract.submit_proposal("P1", program_id, "Provide a documented neighborhood learning session with public materials.", expenses)


def _map(contract, vm, proposer, proposal_id, category="EDU"):
    vm.sender = proposer
    vm.mock_llm(r".*Map each proposed expense.*", json.dumps({"assignments": [{"expense_id": "E1", "category_id": category}]}))
    return contract.map_and_check(proposal_id)


def test_publishes_program(contract, direct_vm, direct_alice, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    assert len(contract.get_program(program_id)["categories"]) == 2


def test_rejects_duplicate_categories(contract, direct_vm, direct_alice, direct_charlie):
    bad = json.dumps({"categories": [{"id": "X", "purpose": "A sufficiently long public purpose description.", "cap_units": 1}, {"id": "X", "purpose": "Another sufficiently long public purpose description.", "cap_units": 2}]})
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid_category"):
        contract.publish_program("BAD", direct_charlie, bad, "A frozen restriction text that is long enough for validation.", "source")


def test_only_proposer_maps(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("only_proposer"):
        contract.map_and_check(proposal_id)


def test_within_caps_ready_for_review(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id)
    assert _map(contract, direct_vm, direct_bob, proposal_id) == "READY_FOR_REVIEW"


def test_over_cap_is_deterministic(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    expenses = json.dumps({"expenses": [{"id": "E1", "description": "Printed learning workbooks for the scheduled class.", "amount_units": 1001}]})
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id, expenses)
    assert _map(contract, direct_vm, direct_bob, proposal_id) == "OVER_CAP"


def test_unmapped_blocks_review(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id)
    assert _map(contract, direct_vm, direct_bob, proposal_id, "UNMAPPED") == "UNMAPPED"


def test_designated_reviewer_authorizes(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id)
    _map(contract, direct_vm, direct_bob, proposal_id)
    direct_vm.sender = direct_charlie
    contract.reviewer_decision(proposal_id, True, "Reviewer authorizes the within-cap public proposal record.")
    assert contract.get_proposal(proposal_id)["state"] == "AUTHORIZED"


def test_bad_model_shape_preserves_submission(contract, direct_vm, direct_alice, direct_bob, direct_charlie):
    program_id = _program(contract, direct_vm, direct_alice, direct_charlie)
    proposal_id = _proposal(contract, direct_vm, direct_bob, program_id)
    direct_vm.sender = direct_bob
    direct_vm.mock_llm(r".*Map each proposed expense.*", json.dumps({"wrong": []}))
    with direct_vm.expect_revert("[LLM_ERROR] wrong_shape"):
        contract.map_and_check(proposal_id)
    assert contract.get_proposal(proposal_id)["state"] == "SUBMITTED"
