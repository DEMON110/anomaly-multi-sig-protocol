# Reproducibility Guide

## Code Pin
- Repo: https://github.com/DEMON110/anomaly-multi-sig-protocol
- Commit: <PIN AFTER YOU COMMIT THESE FILES>
- Release tag (recommended): v0.1.0-alpha


# Reproducibility Details

This document provides the necessary information to ensure reproducibility of experiments, including the required seed values and contract addresses.

## Reproducibility Box — Public Artefacts Repository

- **Primary commit**: fb7af68b8915209f321c357b2eafbde6bb6065d6 
- **Release tag**:  v0.1.0-alpha 
- **Licence**: MIT Licence
- **Chain ID**: 5

### Contracts
- **Policy Multisig**: 0x3551B059C2a9c4c301E8590D72a112f7aB9Fcb74
- **Target Executor**: 0x90486f4b2703d5d40d7b3fdc1e02e20e8e6a9393

### Compiler
- **Solidity Version**:  Solidity 0.8.19
- **Optimizer**: optimizer enabled, runs=200

### Client and RPC
- **Client**:  Infura 
- **Endpoint**: (https://goerli.infura.io/v3/ )

### Seed Values
- **Training Seed**: 42  
- **Evaluation Seed**: 123  
- **Bootstrap Seed**: 456

These seed values ensure that the random processes used in the experiments are consistent across different runs.

## Additional Notes
- Make sure the target executor address is valid and has the necessary permissions to execute actions in the smart contract.
- Replace the placeholders with actual values used in your implementation (e.g., contract address, chain ID, etc.).

random.seed(training_seed)
np.random.seed(training_seed)
