const { ethers } = require("ethers");
const ChildBounty = require("./artifacts/contracts/ChildBounty.sol/ChildBounty.json");

async function main() {
    const provider = new ethers.providers.JsonRpcProvider("YOUR_INFURA_URL");
    const wallet = new ethers.Wallet("YOUR_PRIVATE_KEY", provider);

    const tokenAddress = "TOKEN_CONTRACT_ADDRESS";
    const parentBounty = "PARENT_BOUNTY_CONTRACT_ADDRESS";
    const solverReward = ethers.utils.parseUnits("0.90", "ether");
    const verifierReward = ethers.utils.parseUnits("0.10", "ether");

    const childBountyFactory = new ethers.ContractFactory(ChildBounty.abi, ChildBounty.bytecode, wallet);
    const childBounty = await childBountyFactory.deploy(tokenAddress, parentBounty, solverReward, verifierReward);
    await childBounty.deployed();

    console.log("Child Bounty deployed at:", childBounty.address);

    // Add funding to the child bounty
    const fundingAmount = ethers.utils.parseUnits("1.00", "ether");
    await childBounty.addFunding({ value: fundingAmount });
    console.log("Funding added to the child bounty.");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});