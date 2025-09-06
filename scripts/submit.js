const hre = require("hardhat");

/**
 * Submit a transaction proposal.
 * Usage:
 *  TO=0xTarget VALUE=0 DATA=0xabcdef ANOMALY=true npm run submit:goerli
 */
async function main() {
  const [deployer] = await hre.ethers.getSigners();

  const CONTRACT = process.env.CONTRACT;       // deployed multisig address
  const TO = process.env.TO;                   // target address
  const VALUE = process.env.VALUE || "0";      // in wei, string
  const DATA = process.env.DATA || "0x";       // calldata
  const ANOMALY = String(process.env.ANOMALY || "false").toLowerCase() === "true";

  if (!CONTRACT || !TO) {
    throw new Error("Set CONTRACT and TO env vars.");
  }

  const msig = await hre.ethers.getContractAt("AnomalyMultiSig", CONTRACT, deployer);
  const tx = await msig.submitTransaction(TO, VALUE, DATA, ANOMALY);
  const rc = await tx.wait();
  const ev = rc.logs.map(l => msig.interface.parseLog(l)).find(e => e && e.name === "Submission");
  if (ev) {
    console.log("Submitted txId:", ev.args.txId.toString(), "anomalyFlag:", ev.args.anomalyFlag);
  } else {
    console.log("Submission event not found; check receipt:", rc.transactionHash);
  }
}

main().catch((e) => { console.error(e); process.exit(1); });
