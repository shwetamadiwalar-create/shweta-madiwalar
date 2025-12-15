# shweta-madiwalar
Enhanced Privacy-Preserving Clustered Hierarchical Blockchain-Enabled Federated Learning (EPP-CHBCFL) for Electronic Health Records using the MIMIC-III dataset
EPP-CHBCFL-Reproducibility/
│
├── configs/                # YAML/JSON experiment configurations
├── data/                   # MIMIC-III preprocessing scripts
├── models/                 # CNN / WideResNet-FWBO models
├── baselines/              # FedAvg, DP-FL, MPC-FL implementations
├── privacy/                # Differential Privacy & MPC modules
├── attacks/                # Gradient poisoning & Byzantine attacks
├── blockchain/             # PoW, PoA, PoS+BFT consensus simulation
├── metrics/                # Accuracy, AUC, F1, communication cost
├── scripts/                # Table/Figure reproduction scripts
├── run_experiment.py       # Main experiment entry point
├── requirements.txt
└── README.md
pip install -r requirements.txt
