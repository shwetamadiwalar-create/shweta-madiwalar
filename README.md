# EPP-CHBCFL – Reproducible Federated Learning Framework

This repository provides a research-grade reference implementation used to reproduce the experimental protocol and results reported in Table 5 of the associated manuscript.
## Scope of This Repository

This codebase is provided for methodological reproducibility and experimental transparency. 
It is not intended as a fully integrated end-to-end production deployment.

The implementation focuses on reproducing the federated learning workflow, baseline comparisons, communication cost, worst-case latency modeling, and attack-resilience trends reported in the paper.


What Is Implemented
## Implemented Components

- Client–server federated learning workflow
- Aggregation strategies (FedAvg-style)
- Non-IID data partitioning
- Adversarial client behavior (Byzantine / poisoning)
- Privacy configuration hooks
- Blockchain consensus latency 
- Communication cost

 ## Not Included

- Full hospital-scale deployment
- Live blockchain network
- Production-ready infrastructure

Blockchain and network behavior are modeled using controlled latency and bandwidth assumptions, as described in the manuscript.

This scope is explicitly aligned with Appendix A of the manuscript 
All baselines and the proposed method are evaluated under the same protocol, as detailed in Appendix A:

Dataset: MIMIC-III (simulated feature structure for public release)

Task: Binary in-hospital mortality prediction

Clients: 10

Non-IID partitioning: Dirichlet (α = 0.5)

Local epochs: 5

Batch size: 64

Optimizer: Adam

Learning rate: 0.001

Rounds: 100

Privacy budget (DP methods): ε = 1.0, δ = 1e-5

Malicious clients: 30% (for attack evaluation)

1. Install dependencies

pip install -r requirements.txt
2.Generate non-IID partitions
python data/partition_dirichlet.py
3.Run federated learning
python scripts/run_fl.py --config configs/fl/epp_chbcfl.yaml
4.Run benchmarks (Table 4)
bash scripts/run_blockchain.sh

2.Network Topology and Roles
The permissioned Blockchain network is implemented using Hyperledger Fabric and consists of:
•	Five peer nodes, each acting as endorsers and committers
•	Three Raft-based orderer nodes, all participating in the Raft consensus protocol
•	One application channel shared across all peers and orderers
•	Dedicated anchor peers configured to improve block dissemination efficiency across organizations
Validator selection and rotation are governed by the proposed policy layer operating above Fabric’s native ordering service, while Fabric’s default endorsement and commit flow is preserved.
3.Network Emulation Parameters
To emulate realistic inter-node communication conditions, all network links are uniformly configured using the Traffic Control Network Emulator (tc netem) with the following parameters:
•	Round-trip time (RTT): approximately 10 ms
•	Jitter: 2 ms
•	Packet loss rate: 0.1%
•	Bandwidth: 100 Mbps
These settings are applied consistently across all inter-node routes to ensure controlled and repeatable network behavior.
4. Workload and Transaction Characteristics
Benchmark workloads consist of federated model-update transactions submitted to the Blockchain network with the following characteristics:
•	Transaction rate: 500 to 10,000 updates per benchmark run
•	Payload size: 1 KB to 10 KB per transaction
•	Invocation method: Python scripts invoking chaincode functions
A deterministic workload generator is used to ensure consistent transaction submission patterns across experiments.
5.Channel and Block Configuration
All experiments use fixed channel and block parameters to eliminate configuration-induced variability:
•	Batch timeout: 2 seconds
•	Maximum transactions per block: 100
•	Block size: 1 MB
•	Read / write / admin policies: Hyperledger Fabric default policies
These parameters remain unchanged across all benchmark runs.
 6.Hardware and Deployment Environment
Each blockchain node is provisioned with:
•	CPU: 8-core processor
•	Memory: 16 GB RAM
•	Storage: SSD
•	Operating system: Linux
All components are deployed in Docker containers, and the overall network lifecycle (startup, teardown, scaling) is managed using Docker Compose.
________________________________________
7.Reproducibility Artifacts
To support independent validation of the reported results, the following artifacts are provided in the supplementary package fabric-benchmark.zip:
•	Cryptographic configuration files (crypto-config.yaml)
•	Channel and orderer configuration files (configtx.yaml)
•	Docker Compose manifests for network deployment
•	Network emulation scripts (tc netem configurations)
•	Python-based benchmark driver (benchmark.py)
Together, these artifacts enable exact reconstruction of the experimental environment and reproduction of the latency, throughput, and block finalization measurements presented in Table 4.
 8 .Reproducibility Statement
All benchmark results are generated under fixed configuration settings and deterministic workload profiles. By releasing the complete set of configuration files, scripts, and network parameters, this study enables transparent and repeatable evaluation of blockchain performance under federated learning workloads.

The complete reproducibility package, including configuration files, reference implementations, and benchmark scripts, is publicly available at: https://github.com/<your-username>/EPP-CHBCFL-Reproducibility

Architectural Implementation and Reproducibility Details
1.Motivation and Scope
This appendix elaborates on the architectural design of the proposed federated learning framework governed by a PoS–BFT overlay deployed on Hyperledger Fabric. The intent is to provide sufficient technical detail to allow independent assessment of feasibility, portability, and reproducibility. Importantly, the proposed approach does not alter or replace any native services of Hyperledger Fabric, including its Raft-based ordering mechanism.

2.Architectural Components
Stake Management via Chaincode
Stake management is realized through a dedicated Fabric chaincode, referred to as stake_cc, which operates as a standard smart contract within the Fabric execution environment. This chaincode maintains stake values, peer reputation indicators, and records of misbehavior events. It exposes a set of callable functions that allow querying and updating stake information as well as maintaining the current validator set.Stake adjustments are governed by participation behavior. Nodes that contribute consistently to federated learning rounds gradually accumulate stake, while peers exhibiting equivocal behavior, repeated inactivity, or invalid endorsements experience proportional stake reduction. All stake updates are recorded on the ledger, ensuring auditability.

3. Off-Chain PoS-Based Validator Selection
Validator selection is performed by an external service that operates independently of Fabric’s internal processes. Using the Fabric SDK, this service periodically retrieves the on-chain stake table maintained by stake_cc. Based on these values, a validator committee is selected using stake-weighted probabilistic sampling, favoring reliable and well-performing participants without creating permanent validator dominance.
The resulting validator set is written back to the ledger through stake_cc and is also exported as a signed configuration file. This configuration is subsequently used to restrict endorsement privileges and to coordinate the BFT pre-validation process.

4. BFT-Based Pre-Validation of Model Updates
To provide resilience against Byzantine behavior, a lightweight pre-validation stage inspired by PBFT is executed by the selected validator committee. Each proposed federated learning model update undergoes a sequence of validation steps, including proposal dissemination, peer agreement, and final commit authorization.
An update is considered valid only when signatures representing at least two-thirds of the total committee stake are collected. Validators that attempt to endorse conflicting or invalid updates are penalized through on-chain stake adjustments. Crucially, this BFT procedure is executed prior to submission to Fabric’s ordering service and does not interfere with Raft-based block ordering.

 5.Integration with Hyperledger Fabric
The PoS–BFT overlay interacts with Hyperledger Fabric exclusively through supported interfaces. Stake management is handled via chaincode, validator authorization is enforced through endorsement policies, and transaction ordering is delegated entirely to Fabric’s native Raft service. Only model updates that have successfully passed BFT pre-validation are packaged as Fabric transactions and submitted for ordering and ledger commitment.
Fabric Component	Integration Mechanism
Membership Service Provider (MSP)	Identity and access control
Chaincode	stake_cc for stake and validator state
Endorsing Peers	Restricted via dynamic endorsement policy
Ordering Service	Native Raft (unmodified)
Ledger	Standard immutable commit
	 BFT-approved federated learning updates are encapsulated as Fabric transactions and forwarded to the Raft ordering service
Validator Rotation and Fault Handling
Validator assignments are periodically refreshed at the beginning of each training epoch to prevent centralization and adapt to changing peer behavior. A short transition window allows newly selected validators to assume responsibility without interrupting ongoing training rounds. Peer liveness is monitored through heartbeat signals, and unresponsive validators are promptly deactivated.
In cases where validator availability temporarily falls below the required safety threshold, the system reverts to a broader endorsement policy until a stable committee is re-established. This mechanism ensures continuity of operation while maintaining security guarantees.

 Configuration and Reproducibility Artifacts
To support reproducibility, the implementation relies on a set of configuration files and scripts that operate entirely within the standard Fabric ecosystem. These artifacts define stake management rules, validator selection parameters, endorsement policies, and network configuration settings. Their modular structure allows the framework to be deployed or adapted across different Fabric-based environments without modification of core components.

 Architectural Summary
The accompanying architecture diagram illustrates the layered design of the system, highlighting the separation between the PoS–BFT governance overlay and the underlying Hyperledger Fabric infrastructure. This separation ensures that enhanced security and fault tolerance are achieved without compromising Fabric’s portability or compatibility.

The complete reproducibility package, including configuration files, reference implementations, and benchmark scripts, is publicly available at: https://github.com/<your-username>/EPP-CHBCFL-Reproducibility

Architectural Components
1. Stake Management through Fabric Chaincode
Stake management is realized using a dedicated Hyperledger Fabric chaincode, denoted as stake_cc, which operates as a standard smart contract within the Fabric execution environment. This chaincode maintains on-ledger records of stake values, peer reputation indicators, and detected misbehavior events. It provides callable interfaces for retrieving stake information, updating reputation scores, and maintaining the current validator committee.
Stake evolution is driven by observed participation patterns during federated learning. Nodes that consistently submit valid and timely model updates accrue stake over time, whereas peers demonstrating equivocation, repeated inactivity, or invalid endorsements incur proportional reductions. All stake updates are immutably committed to the ledger, enabling transparent auditing and verifiable tracking of validator eligibility.

2. Off-Chain Proof-of-Stake Validator Selection
Validator selection is carried out by an off-chain policy service that functions independently of Fabric’s internal execution flow. Through the Fabric SDK, this service periodically queries the on-chain stake table maintained by stake_cc. Based on the retrieved values, a validator committee is formed using stake-weighted probabilistic selection, promoting reliable contributors while preventing persistent validator dominance.
The resulting validator set is committed back to the ledger via stake_cc and simultaneously exported as a signed configuration artifact. This artifact is subsequently used to enforce endorsement restrictions and to coordinate the Byzantine Fault Tolerant (BFT) pre-validation stage.

3. BFT-Based Pre-Validation of Federated Learning Updates
To mitigate Byzantine behavior, a lightweight BFT-inspired pre-validation phase is executed by the selected validator committee. Each proposed federated learning update undergoes a structured validation sequence involving proposal dissemination, agreement checking, and final authorization.
A model update is accepted only when cryptographic signatures representing at least two-thirds of the committee’s total stake are collected. Validators attempting to approve conflicting or invalid updates are penalized via corresponding on-chain stake adjustments. This pre-validation stage is performed before submission to Fabric’s ordering service and therefore does not interfere with the native Raft-based block ordering process.

4. Integration with Hyperledger Fabric
The PoS–BFT governance overlay interfaces with Hyperledger Fabric solely through supported and standard extension mechanisms. Stake accounting is implemented through chaincode, validator permissions are enforced using dynamic endorsement policies, and transaction ordering is delegated entirely to Fabric’s native Raft ordering service.
No modifications are introduced to Fabric’s core components, including the peer runtime, ordering service, or consensus logic. Only federated learning updates that successfully pass BFT pre-validation are packaged as Fabric transactions and submitted for ordering and immutable ledger commitment.
Fabric Component	Integration Mechanism
Membership Service Provider (MSP)	Identity and access control
Chaincode	stake_cc for stake and validator state
Endorsing Peers	Restricted via dynamic endorsement policy
Ordering Service	Native Raft (unmodified)
Ledger	Standard immutable commit
	
5 Validator Rotation and Fault Handling
Validator assignments are periodically refreshed at the start of each training epoch to reduce centralization risks and to adapt to changing peer behavior. A brief transition interval allows newly selected validators to assume responsibilities without disrupting ongoing training rounds.
Peer liveness is continuously monitored using heartbeat mechanisms. Validators that become unresponsive are promptly removed from the active committee. If validator availability temporarily drops below the required safety threshold, the system automatically reverts to a broader endorsement policy until a stable committee is restored, thereby preserving operational continuity while maintaining security guarantees.
6 Configuration and Reproducibility Artifacts
The implementation is supported by a modular collection of configuration files and scripts that operate entirely within the standard Hyperledger Fabric ecosystem. These artifacts specify stake management logic, validator selection parameters, endorsement policies, and network configuration settings.
The framework has been validated on unmodified Hyperledger Fabric v2.x deployments, ensuring portability across standard Fabric environments. Its modular structure allows deployment and adaptation without altering any core Fabric components.

7 Architectural Summary
The accompanying architecture diagram illustrates the layered design of the proposed system, clearly distinguishing the PoS–BFT governance overlay from the underlying Hyperledger Fabric infrastructure. This separation enables enhanced security, fault tolerance, and trust-aware aggregation while preserving Fabric’s compatibility, portability, and native consensus behavior.
The complete reproducibility package—including configuration files, reference implementations, and benchmark scripts—is publicly available at:
https://github.com/<your-username>/EPP-CHBCFL-Reproducibility


<img width="734" height="344" alt="image" src="https://github.com/user-attachments/assets/0a3a1b67-f766-47bc-ab70-331919e01696" />





