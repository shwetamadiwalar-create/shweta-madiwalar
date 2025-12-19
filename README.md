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


<img width="734" height="344" alt="image" src="https://github.com/user-attachments/assets/0a3a1b67-f766-47bc-ab70-331919e01696" />





