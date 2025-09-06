const hre = require("hardhat");

/**
 * Confirm a pending transaction.
 * Usage:
 *  CONTRACT=0xMultisig TXID=0 npm run confirm:goerli
 */
async function main() {
  const [actor] = await hre.ethers.getSigners();
  const CONTRACT = process.env.CONTRACT;
  const TXID = parseInt(process.env.TXID || "-1", 10);
  if (!CONTRACT || TXID < 0) throw new Error("Set CONTRACT and TXID env vars.");

  const msig = await hre.ethers.getContractAt("AnomalyMultiSig", CONTRACT, actor);
  const tx = await msig.confirmTransaction(TXID);
  await tx.wait();
  console.log("Confirmed txId:", TXID, "by", actor.address);
}

main().catch((e) => { console.error(e); process.exit(1); });
