// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract ChildBounty is Ownable {
    IERC20 public immutable token;
    address public parentBounty;
    uint256 public solverReward;
    uint256 public verifierReward;
    uint256 public totalFunding;
    bool public isClaimable;
    bool public isSettled;

    event FundingAdded(uint256 amount);
    event BountyBecameClaimable();
    event BountySettled(address indexed solver, uint256 amount);

    constructor(
        IERC20 _token,
        address _parentBounty,
        uint256 _solverReward,
        uint256 _verifierReward
    ) {
        token = _token;
        parentBounty = _parentBounty;
        solverReward = _solverReward;
        verifierReward = _verifierReward;
    }

    function addFunding() external payable {
        require(msg.value >= solverReward, "Funding must cover solver reward");
        totalFunding += msg.value;
        emit FundingAdded(msg.value);
        if (totalFunding >= solverReward &&!isClaimable) {
            isClaimable = true;
            emit BountyBecameClaimable();
        }
    }

    function claimBounty() external {
        require(isClaimable, "Bounty is not claimable");
        require(!isSettled, "Bounty is already settled");

        // Transfer the solver reward to the caller
        token.transfer(msg.sender, solverReward);

        // Settle the bounty
        isSettled = true;
        emit BountySettled(msg.sender, solverReward);
    }

    function getFundingStatus() external view returns (uint256, bool) {
        return (totalFunding, isClaimable);
    }
}