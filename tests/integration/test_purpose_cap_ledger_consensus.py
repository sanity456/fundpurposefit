import hashlib
import json
from pathlib import Path

from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def _context(fragment, response):
    validators = get_validator_factory().batch_create_mock_validators(
        5,
        mock_llm_response={"nondet_exec_prompt": {fragment: json.dumps(response)}},
    )
    return {
        "validators": [validator.to_dict() for validator in validators],
        "genvm_datetime": "2026-08-25T12:00:00Z",
    }


def _deploy(contract_file, owner_account):
    factory = get_contract_factory(
        contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / contract_file
    )
    receipt = factory.deploy_contract_tx(
        args=[],
        account=owner_account,
        wait_transaction_status=TransactionStatus.FINALIZED,
    )
    _ok(receipt)
    return factory, extract_contract_address(receipt)


def _send(method, args, context=None):
    if context is None:
        receipt = method(args=args).transact(
            wait_transaction_status=TransactionStatus.FINALIZED
        )
    else:
        receipt = method(args=args).transact(
            transaction_context=context,
            wait_transaction_status=TransactionStatus.FINALIZED,
        )
    _ok(receipt)
    return receipt


def test_five_validator_purpose_cap_and_reviewer_flow():
    publisher_account, proposer_account, reviewer_account = create_accounts(3)
    factory, address = _deploy("purpose_cap_ledger.py", publisher_account)
    publisher = factory.build_contract(address, account=publisher_account)
    proposer = factory.build_contract(address, account=proposer_account)
    reviewer = factory.build_contract(address, account=reviewer_account)
    program_id = f"{str(publisher_account.address).lower()}:COMMUNITY"
    proposal_id = f"{str(proposer_account.address).lower()}:P1"
    categories = json.dumps({"categories": [
        {"id": "EDU", "purpose": "Direct community education materials and facilitated learning sessions.", "cap_units": 1000},
        {"id": "OPS", "purpose": "Documented operational supplies supporting the registered program.", "cap_units": 500},
    ]})
    expenses = json.dumps({"expenses": [{"id": "E1", "description": "Printed learning workbooks for the scheduled class.", "amount_units": 400}]})
    _send(publisher.publish_program, ["COMMUNITY", reviewer_account.address, categories, "Funds may support only the two frozen public purpose categories and their stated caps.", "donor-restriction-snapshot"])
    _send(proposer.submit_proposal, ["P1", program_id, "Provide a documented neighborhood learning session with public materials.", expenses])
    _send(proposer.map_and_check, [proposal_id], _context("Map each proposed expense", {"assignments": [{"expense_id": "E1", "category_id": "EDU"}]}))
    _send(reviewer.reviewer_decision, [proposal_id, True, "Reviewer authorizes the within-cap public proposal record."])
    assert proposer.get_proposal(args=[proposal_id]).call()["state"] == "AUTHORIZED"
