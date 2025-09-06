const hre = require("hardhat");

async function main() {
  const signersCsv = process.env.SIGNERS || "";
  const thresholdStr = process.env.THRESHOLD || "2";
  const owners = signersCsv.split(",").map(s => s.trim()).filter(Boolean);
  const threshold = parseInt(thresholdStr, 10);

  if (owners.length === 0) {
    throw new Error("SIGNERS env var is required (comma-separated addresses)");
  }
  if (!Number.isInteger(threshold) || threshold < 1 || threshold > owners.length) {
    throw new Error("THRESHOLD must be an integer 1..owners.length");
  }

  const Factory = await hre.ethers.getContractFactory("AnomalyMultiSig");
  const contract = await Factory.deploy(owners, threshold);
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("AnomalyMultiSig deployed to:", address);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
