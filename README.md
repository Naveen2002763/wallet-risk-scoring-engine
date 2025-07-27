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
│ └── feature_engineering.py # Risk score calculator
├── README.md
├── requirements.txt

## Set Your Etherscan API Key
Before running the project, you must set your own Etherscan API key. This is necessary to fetch wallet transactions from the Ethereum blockchain. If this step is skipped, the data fetching script will not work.

## 🧭 How to Get Your API Key
* Go to https://etherscan.io/register

* Create an account or log in

* Click on your profile icon (top-right corner)

* Select API Dashboard

* Scroll down to the API Keys section

* Click the “+ Add” button on the right

* Give your key a name (e.g., wallet_key) and click Create

* Copy the generated key — you will need it in the next step

## 🛠️ How to Set Your API Key (Choose Any One Method)
You can use any one of the following three methods to provide your API key securely.

## Method 1: Set Temporarily via Terminal
Use this method if you want to run the script just once and test it quickly.

 On Windows, open Command Prompt or VS Code terminal and run:
set ETHERSCAN_API_KEY=your_api_key_here

* On Mac/Linux, open Terminal and run:
export ETHERSCAN_API_KEY=your_api_key_here

* This key will stay active only until you close that terminal window.

* To check if it was saved correctly, run:

* On Windows:
echo %ETHERSCAN_API_KEY%

* On Mac/Linux:
echo $ETHERSCAN_API_KEY

* In your Python script, the key is accessed as:
import os
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

## Method 2: Save Permanently on Mac/Linux Systems
* Use this if you want to avoid setting the key every time.

* Open your Terminal app (or terminal in VS Code).

* Run this command to save it permanently:
echo 'export ETHERSCAN_API_KEY=your_api_key_here' >> ~/.bashrc

* Then activate it:
source ~/.bashrc

💡 If you are using Zsh (common on newer Macs), replace .bashrc with .zshrc.

* To confirm it's stored, run:
echo $ETHERSCAN_API_KEY

* Your Python code remains the same:
import os
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

## Method 3: Store in a Config File (Beginner Friendly)
* You can create a simple config.txt file in the root folder of this project and write your API key inside it like:
ETHERSCAN_API_KEY=your_api_key_here

* Then in your Python script, read the key using:
with open("config.txt") as f:
 ETHERSCAN_API_KEY = f.read().split("=")[1].strip()

* Make sure you add this config.txt file to your .gitignore to prevent accidental uploads to GitHub.

🔒 Security Note
* Never copy-paste your API key directly into the main Python files. Use any of the three secure options above to keep your credentials safe and private.
---

## 🚀 How to Run
```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Fetch transactions
python scripts/fetch_transactions.py

# Step 3: Compute wallet risk scores
python scripts/score_engine.py
```
---

## 📤 Final Output
The final output is a CSV with the following format:
wallet_id	score
0xfaa0768bde629806739c3a4620656c5d26f44ef2	732
Located at: output/wallet_scores.csv

---

## 👨‍💻 Author
Name: Nadipena Naveen
GitHub: [https://github.com/Naveen2002763]
