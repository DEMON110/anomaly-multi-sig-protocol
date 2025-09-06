// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title AnomalyMultiSig
 * @notice Minimal, dependency-free multisig with an "anomalyFlag" on each proposal.
 *         - Owners: fixed set at construction.
 *         - Threshold: t-of-n confirmations required to execute.
 *         - Propose -> Confirm -> Execute flow.
 *         - Each proposal carries an anomalyFlag (e.g., true if your off-chain model marks it suspicious at τ*).
 */
contract AnomalyMultiSig {
    /*//////////////////////////////////////////////////////////////
                                EVENTS
    //////////////////////////////////////////////////////////////*/
    event Submission(uint256 indexed txId, address indexed proposer, bool anomalyFlag);
    event Confirmation(address indexed owner, uint256 indexed txId);
    event Revocation(address indexed owner, uint256 indexed txId);
    event Execution(uint256 indexed txId, bool success, bytes returnData);

    /*//////////////////////////////////////////////////////////////
                                STORAGE
    //////////////////////////////////////////////////////////////*/
    address[] public owners;
    mapping(address => bool) public isOwner;
    uint256 public threshold;

    struct Transaction {
        address to;
        uint256 value;
        bytes data;
        bool executed;
        bool anomalyFlag; // off-chain anomaly label at proposal time
        uint256 confirmations;
        mapping(address => bool) approvedBy;
    }

    // txId => Transaction
    mapping(uint256 => Transaction) private _txs;
    uint256 public txCount;

    /*//////////////////////////////////////////////////////////////
                              MODIFIERS
    //////////////////////////////////////////////////////////////*/
    modifier onlyOwner() {
        require(isOwner[msg.sender], "not owner");
        _;
    }

    modifier txExists(uint256 txId) {
        require(txId < txCount, "tx does not exist");
        _;
    }

    modifier notExecuted(uint256 txId) {
        require(!_txs[txId].executed, "tx executed");
        _;
    }

    modifier notConfirmed(uint256 txId) {
        require(!_txs[txId].approvedBy[msg.sender], "already confirmed");
        _;
    }

    /*//////////////////////////////////////////////////////////////
                               CONSTRUCTOR
    //////////////////////////////////////////////////////////////*/
    constructor(address[] memory _owners, uint256 _threshold) {
        require(_owners.length > 0, "owners required");
        require(_threshold > 0 && _threshold <= _owners.length, "bad threshold");
        for (uint256 i = 0; i < _owners.length; i++) {
            address owner = _owners[i];
            require(owner != address(0), "zero owner");
            require(!isOwner[owner], "owner not unique");
            isOwner[owner] = true;
            owners.push(owner);
        }
        threshold = _threshold;
    }

    /*//////////////////////////////////////////////////////////////
                            PUBLIC/EXTERNAL
    //////////////////////////////////////////////////////////////*/

    /**
     * @notice Propose a transaction. Attach anomalyFlag according to off-chain detection at τ*.
     */
    function submitTransaction(
        address to,
        uint256 value,
        bytes calldata data,
        bool anomalyFlag
    ) external onlyOwner returns (uint256 txId) {
        txId = txCount;
        txCount += 1;

        Transaction storage t = _txs[txId];
        t.to = to;
        t.value = value;
        t.data = data;
        t.anomalyFlag = anomalyFlag;

        emit Submission(txId, msg.sender, anomalyFlag);
    }

    /**
     * @notice Confirm a transaction.
     */
    function confirmTransaction(uint256 txId)
        external
        onlyOwner
        txExists(txId)
        notExecuted(txId)
        notConfirmed(txId)
    {
        Transaction storage t = _txs[txId];
        t.approvedBy[msg.sender] = true;
        t.confirmations += 1;

        emit Confirmation(msg.sender, txId);
    }

    /**
     * @notice Revoke a previous confirmation.
     */
    function revokeConfirmation(uint256 txId)
        external
        onlyOwner
        txExists(txId)
        notExecuted(txId)
    {
        Transaction storage t = _txs[txId];
        require(t.approvedBy[msg.sender], "not confirmed");
        t.approvedBy[msg.sender] = false;
        t.confirmations -= 1;

        emit Revocation(msg.sender, txId);
    }

    /**
     * @notice Execute a confirmed transaction.
     */
    function executeTransaction(uint256 txId)
        external
        onlyOwner
        txExists(txId)
        notExecuted(txId)
    {
        Transaction storage t = _txs[txId];
        require(t.confirmations >= threshold, "insufficient confirmations");
        t.executed = true;

        (bool ok, bytes memory ret) = t.to.call{value: t.value}(t.data);
        emit Execution(txId, ok, ret);
        require(ok, "call failed");
    }

    /*//////////////////////////////////////////////////////////////
                                VIEWS
    //////////////////////////////////////////////////////////////*/
    function getTransaction(uint256 txId)
        external
        view
        returns (
            address to,
            uint256 value,
            bytes memory data,
            bool executed,
            bool anomalyFlag,
            uint256 confirmations
        )
    {
        Transaction storage t = _txs[txId];
        return (t.to, t.value, t.data, t.executed, t.anomalyFlag, t.confirmations);
    }

    receive() external payable {}
}
