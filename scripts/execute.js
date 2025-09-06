const hre = require("hardhat");

/**
 * Execute a confirmed transaction.
 * Usage:
 *  CONTRACT=0xMultisig TXID=0 npm run execute:goerli
 */
async function main() {
  const [actor] = await hre.ethers.getSigners();
  const CONTRACT = process.env.CONTRACT;
  const TXID = parseInt(process.env.TXID || "-1", 10);
  if (!CONTRACT || TXID < 0) throw new Error("Set CONTRACT and TXID env vars.");

  const msig = await hre.ethers.getContractAt("AnomalyMultiSig", CONTRACT, actor);
  const tx = await msig.executeTransaction(TXID);
  const rc = await tx.wait();
  console.log("Executed txId:", TXID, "txHash:", rc.hash);
}

main().catch((e) => { console.error(e); process.exit(1); });
