# anomaly-multi-sig-protocol
Anomaly-Aware Multi-Signature Protocol
This repository implements an anomaly-aware multi-signature protocol on the Ethereum Goerli testnet, with cross-chain support for secure transaction validation and anomaly detection.
Reproducibility Box — Environment Artefacts
To ensure reproducibility for our Q1 journal submission, the following artefacts describe the project’s environment:

Repository: https://github.com/DEMON110/anomaly-multi-sig-protocol.git
Commit: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
Chain ID: 5 (Ethereum Goerli testnet)
Compiler: Solidity 0.8.19
Optimizer: Enabled, runs=200
Contracts: 0x1234567890abcdef1234567890abcdef12345678
Signers:
n = 3
t = 2


epochId: 1
RPC Provider: Infura (https://goerli.infura.io/v3/)

Setup Instructions

Clone the repository:git clone https://github.com/DEMON110/anomaly-multi-sig-protocol.git
cd anomaly-multi-sig-protocol


Install dependencies:npm install


Configure Goerli network in hardhat.config.js:require("dotenv").config();
module.exports = {
  solidity: "0.8.19",
  networks: {
    goerli: {
      url: process.env.GOERLI_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};

# 0) install
npm i

# 1) copy .env.example -> .env and fill values
cp .env.example .env

# 2) compile
npm run compile

# 3) deploy (example: Goerli)
npm run deploy:goerli
# -> prints deployed address; export it for the next steps
export CONTRACT=0xYourDeployedMsig

# 4) submit a transaction (no value, arbitrary calldata, mark anomaly=true)
export TO=0xTargetContract
export VALUE=0
export DATA=0x
export ANOMALY=true
npm run submit:goerli
# -> note txId from console (e.g., 0)

# 5) confirmations (run from 2 distinct owner keys)
export TXID=0
npm run confirm:goerli

# 6) execute (after reaching threshold)
npm run execute:goerli


Obtain test ETH from https://goerlifaucet.com/.
Deploy contracts:npx hardhat run scripts/deploy.js --network goerli


Verify contracts on Goerli Etherscan:npx hardhat verify --network goerli <contract-address> <constructor-args>



Usage

Multi-Signature Wallet: Deployed at [contract-address], requires t = 2 signatures from n = 3 signers to execute transactions.
Anomaly Detection: Monitors transaction patterns for suspicious activity (e.g., unusual gas usage or signer behavior).
Cross-Chain Support: Integrates with [e.g., Chainlink CCIP] for interoperability with other blockchains.

