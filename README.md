
pip install -r requirements.txt
EPP-CHBCFL/
│
├── README.md
├── LICENSE
├── requirements.txt
├── CITATION.cff
│
├── configs/
│   ├── fl/
│   │   ├── fedavg.yaml
│   │   ├── fedprox.yaml
│   │   ├── static_hfl.yaml
│   │   ├── dynamic_hfl.yaml
│   │   ├── dp_fl.yaml
│   │   ├── bfl.yaml
│   │   ├── c_bfl.yaml
│   │   └── epp_chbcfl.yaml
│   │
│   ├── blockchain/
│   │   ├── crypto-config.yaml
│   │   ├── configtx.yaml
│   │   ├── docker-compose.yaml
│   │   └── validator_policy.yaml
│
├── data/
│   ├── README.md
│   ├── partition_dirichlet.py
│   └── seed_list.txt
│
├── models/
│   ├── cnn_model.py
│   ├── aggregation.py
│   └── clustering.py
│
├── privacy/
│   ├── differential_privacy.py
│   └── privacy_utils.py
│
├── blockchain/
│   ├── validator_selection.py
│   ├── consensus_utils.py
│   └── ledger_interface.py
│
├── benchmark/
│   ├── benchmark.py
│   ├── latency_measurement.py
│   ├── throughput_measurement.py
│   └── tc_netem.sh
│
├── scripts/
│   ├── run_fl.py
│   ├── run_blockchain.sh
│   ├── run_benchmark.sh
│   └── reproduce_tables.sh
│
├── results/
│   ├── table3_scalability.csv
│   ├── table4_blockchain_latency.csv
│   └── attack_results.csv
│
└── supplementary/
    ├── Appendix_A_Reproducibility.pdf
    └── Benchmark_Profile.pdf

 
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

📁 Benchmark Configuration

Peers: 5

Orderers: 3 (Raft)

Block size: 1 MB

Batch timeout: 2 seconds

Payload size: 1–10 KB

Transactions: 500–10,000 per run

Network conditions are emulated using tc netem.

 requirements.txt
numpy
pandas
scikit-learn
torch
torchvision
flwr
opacus
matplotlib
docker
pyyaml
data/README.md

This folder contains scripts for dataset partitioning.
- Dirichlet-based non-IID partitioning (α = 0.5)
- Fixed seed list for reproducibility
- Compatible with healthcare datasets (e.g., EHR, ECG)

benchmark/tc_netem.sh
tc qdisc add dev eth0 root netem delay 11ms 3ms loss 0.1%
tc qdisc add dev eth0 parent root handle 1: tbf rate 100mbit burst 32kbit latency 400ms

scripts/reproduce_tables.sh
echo "Reproducing Table 3 (Scalability)..."
python scripts/run_fl.py --all_baselines

echo "Reproducing Table 4 (Blockchain Benchmark)..."
python benchmark/benchmark.py

