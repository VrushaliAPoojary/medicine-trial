const hre = require("hardhat");

async function main() {
  const TrialManager = await hre.ethers.getContractFactory("TrialManager");
  const trialManager = await TrialManager.deploy();

  await trialManager.deployed();

  console.log(`TrialManager deployed at: ${trialManager.address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
