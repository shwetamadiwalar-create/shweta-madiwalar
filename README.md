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
8.Reproducibility Statement
All benchmark results are generated under fixed configuration settings and deterministic workload profiles. By releasing the complete set of configuration files, scripts, and network parameters, this study enables transparent and repeatable evaluation of blockchain performance under federated learning workloads.

The complete reproducibility package, including configuration files, reference implementations, and benchmark scripts, is publicly available .
