const { ethers } = require("ethers");
const ParentBounty = require("./artifacts/contracts/ParentBounty.sol/ParentBounty.json");

async function main() {
    const provider = new ethers.providers.JsonRpcProvider("YOUR_INFURA_URL");
    const wallet = new ethers.Wallet("YOUR_PRIVATE_KEY", provider);

    const parentBountyAddress = "PARENT_BOUNTY_CONTRACT_ADDRESS";
    const childBountyAddress = "CHILD_BOUNTY_CONTRACT_ADDRESS";

    const parentBounty = new ethers.Contract(parentBountyAddress, ParentBounty.abi, wallet);

    // Add the child bounty to the parent bounty
    await parentBounty.addChildBounty(childBountyAddress);
    console.log("Child bounty added to the parent bounty.");
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});