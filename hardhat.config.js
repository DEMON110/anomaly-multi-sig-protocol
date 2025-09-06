require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

const { GOERLI_RPC_URL, SEPOLIA_RPC_URL, HOLESKY_RPC_URL, PRIVATE_KEY } = process.env;

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.19",
    settings: { optimizer: { enabled: true, runs: 200 } }
  },
  networks: {
    hardhat: {},
    goerli: GOERLI_RPC_URL ? {
      url: GOERLI_RPC_URL,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : []
    } : undefined,
    sepolia: SEPOLIA_RPC_URL ? {
      url: SEPOLIA_RPC_URL,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : []
    } : undefined,
    holesky: HOLESKY_RPC_URL ? {
      url: HOLESKY_RPC_URL,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : []
    } : undefined
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY || process.env.ETHERSCAN_KEY || ""
  }
};
