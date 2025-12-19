
Experimental Protocol (Unified)

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

This repository provides the full reproducibility package for the paper:

“Enhanced Privacy-Preserving Clustered Hierarchical Blockchain-Enabled Federated Learning for Healthcare"

It includes implementation scripts, configuration files, network emulation settings, and benchmark tools used to generate Tables 3 and 4.

 Key Features
- Dynamic hierarchical clustering using fixed distance metrics and linkage
- Blockchain-governed aggregation and validator selection
- Differential privacy support (ε = 1.0)
- Explicit comparative baselines (FedAvg, HFL, BFL, etc.)
- Worst-case latency benchmarking under realistic hospital networks


Experimental Protocol
Seeds: 5 random seeds
Non-IID partitions: 3 Dirichlet splits (α = 0.5)
Total runs per setting: 15
Network emulation:RTT 10–12 ms, jitter 2–3 ms, packet loss 0.1%

1. Install dependencies

pip install -r requirements.txt
2.Generate non-IID partitions
python data/partition_dirichlet.py
3.Run federated learning
python scripts/run_fl.py --config configs/fl/epp_chbcfl.yaml
4.Run benchmarks (Table 4)
bash scripts/run_blockchain.sh



