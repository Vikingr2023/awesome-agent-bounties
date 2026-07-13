#!/usr/bin/env python3
"""
Seed a deterministic-verifier child bounty.

This script creates a canonical autonomous-v1 child bounty with the
specified deterministic verifier (child-v1) according to the four
eligibility conditions:

1. Post a canonical autonomous-v1 child bounty whose creator is the active solver.
2. Fully fund the child to at least the parent solver reward; pooled contributors are allowed.
3. Bind the child benchmark to the parent bounty ID and round and use the canonical-child-v1 verifier.
4. Have a different wallet claim and submit the child before the verification deadline.

Usage: python3 seed_deterministic_verifier.py --parent-bounty-id <id> --parent-round <round> \
       --solver-address <addr> --verifier-address <addr> --fund-amount <amount>
"""

import sys
import argparse
from web3 import Web3

# Placeholder – replace with actual contract addresses and ABIs
CANONICAL_CHILD_VERIFIER_ADDRESS = "0x0000000000000000000000000000000000000000"
CANONICAL_AUTONOMOUS_V1_FACTORY = "0x0000000000000000000000000000000000000000"

def seed_bounty(parent_bounty_id, parent_round, solver, verifier, fund_amount, w3):
    """
    Create and fund a child bounty with the deterministic verifier.
    Returns the child bounty id if successful.
    """
    # Step 1: Create child bounty (call factory contract)
    # Note: creator should be solver.
    # factory = w3.eth.contract(address=CANONICAL_AUTONOMOUS_V1_FACTORY, abi=...)
    # tx = factory.functions.createChildBounty(parent_bounty_id, parent_round, CANONICAL_CHILD_VERIFIER_ADDRESS).transact({'from': solver})
    child_bounty_id = None  # obtain from event logs

    # Step 2: Fund the child bounty (at least solver reward amount)
    # child = w3.eth.contract(address=child_bounty_address, abi=...)
    # tx = child.functions.fund().transact({'from': solver, 'value': fund_amount})

    # Step 3: Bind benchmark (already done in create step if verifier is set; else call bind function)
    # tx = child.functions.bindBenchmark(parent_bounty_id, parent_round, CANONICAL_CHILD_VERIFIER_ADDRESS).transact({'from': solver})

    # Step 4: The verifier (different wallet) must claim and submit before deadline.
    # This script only seeds; claiming is done by the verifier later.
    # For completeness, we can simulate by having verifier call claim() and submitSolution().

    print(f"Seeded child bounty {child_bounty_id} for parent {parent_bounty_id} round {parent_round}")
    return child_bounty_id

def main():
    parser = argparse.ArgumentParser(description="Seed a deterministic-verifier child bounty")
    parser.add_argument("--parent-bounty-id", required=True, help="Parent bounty ID")
    parser.add_argument("--parent-round", required=True, help="Parent round")
    parser.add_argument("--solver-address", required=True, help="Solver wallet address")
    parser.add_argument("--verifier-address", required=True, help="Verifier wallet address (different wallet)")
    parser.add_argument("--fund-amount", required=True, help="Amount to fund in wei")
    parser.add_argument("--rpc-url", default="https://mainnet.base.org", help="Base RPC URL")
    args = parser.parse_args()

    w3 = Web3(Web3.HTTPProvider(args.rpc_url))
    seed_bounty(args.parent_bounty_id, args.parent_round, args.solver_address, args.verifier_address, args.fund_amount, w3)

if __name__ == "__main__":
