// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
  const currentTimestampInSeconds = Math.round(Date.now() / 1000);
  const unlockTime = currentTimestampInSeconds + 60;

  const lockedAmount = hre.ethers.utils.parseEther("0.001");

  const contractFactory = await hre.ethers.getContractFactory("KZC");
  //const contract = await contractFactory.deploy(unlockTime, { value: lockedAmount });
  const contract = await contractFactory.deploy();

  await contract.deployed();

  console.log(
    `Lock with ${ethers.utils.formatEther(
      lockedAmount
    )}ETH and unlock timestamp ${unlockTime} deployed to ${contract.address}`
  );

  console.log(network.config);

  if (network.config.chainId == 97) {
    contract.deployTransaction.wait(6);
    verify(contract.address, []);
  }

}

async function verify(contractAddress, arguments) {
  try {
    await run("verify:verify", {
      address: contractAddress,
      constructorArguments: arguments,
    });
  } catch (e) {
    if (e.message.toLowerCase().includes("already verified")) {
      console.log("The contract already verified");
    } else {
      console.log(e);
    }
  }
}


// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
