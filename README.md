# wallet-risk-scoring-engine
# 🛡️ Wallet Risk Scoring Engine (ETH/Aave-based)
This repository implements a robust wallet risk scoring system that evaluates on-chain wallet behavior using data from Etherscan. It applies heuristic-based features derived from Aave-compatible transactional behavior and assigns scores from **0 to 1000**.

---

## 📌 Problem Statement
Given 100+ wallet addresses, evaluate their on-chain activity and assign a risk score that reflects their reliability and behavioral pattern.

---

## 📥 Data Collection Method
- Used **Etherscan API** to fetch full transaction history (`txlist`) of each wallet (up to 10,000 txns).
- Rate-limited at 5 req/sec to comply with free-tier API policies.
- Saved transaction data in JSON format for reuse.

---

## 🔍 Feature Selection Rationale
From each wallet’s transaction history, the following key behavioral metrics were extracted:

| Feature               | Reason |
|-----------------------|--------|
| **txn_count**         | Measures wallet activity (log-scaled) |
| **total_value (ETH)** | Reflects total economic throughput |
| **avg_value (ETH)**   | Indicates average trust per transaction |
| **unique_recipients** | Shows diversity of counterparties |
| **unique_methods**    | Captures smart contract interaction diversity |
| **success_rate**      | Rewards clean execution history (fewer failures) |

---

## 🧠 Scoring Method
Each wallet was scored using a weighted formula:
score =
* log1p(txn_count) × 60 → (up to 200 points)
  
* sqrt(total_value) × 40 → (up to 200 points)

* unique_recipients × 4 → (up to 100 points)

* unique_methods × 6 → (up to 100 points)

* log1p(avg_value) × 60 → (up to 200 points)

* success_rate × 200 → (up to 200 points)

- Final score is **clamped between 0–1000**
- Small ± perturbation introduced to de-duplicate scores repeated >3 times

---

## ✅ Justification of Risk Indicators
These features cover a wallet’s:
- Activity (transaction count)
- Value circulation (total + average ETH)
- Smart contract trust (methods used)
- Clean behavior (success ratio)
- Breadth of counterparties

This makes the model scalable, interpretable, and suited for DeFi use cases such as Aave, Compound, and lending platforms.

---

## 📂 Folder Structure
├── data/ # Input wallet list
├── output/ # Fetched txns + risk scores
├── scripts/
│ ├── fetch_transactions.py # Data fetch logic
│ └── score_engine.py # Risk score calculator
├── README.md
├── requirements.txt


---

## 🚀 How to Run
```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Fetch transactions
python scripts/fetch_transactions.py

# Step 3: Compute wallet risk scores
python scripts/score_engine.py

---

## 📤 Final Output
The final output is a CSV with the following format:
wallet_id	score
0xfaa0768bde629806739c3a4620656c5d26f44ef2	732
Located at: output/wallet_scores.csv

👨‍💻 Author
Name: Nadipena Naveen
GitHub: [https://github.com/Naveen2002763]
