import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from collections import defaultdict

# === File Paths ===
TXN_PATH = r"C:\Users\Jabili N\Music\zeru_wallet_risk_project\output\wallet_transactions.json"
OUTPUT_PATH = r"C:\Users\Jabili N\Music\zeru_wallet_risk_project\output\wallet_scores.csv"

# === Step 1: Load Transaction JSON ===
with open(TXN_PATH, "r") as file:
    wallet_data = json.load(file)

# === Step 2: Flatten JSON to DataFrame ===
all_txns = []
for wallet_id, txns in wallet_data.items():
    for txn in txns:
        txn["wallet_id"] = wallet_id
        all_txns.append(txn)

df = pd.DataFrame(all_txns)

# === Step 3: Numeric Cleanup ===
df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)
df["isError"] = pd.to_numeric(df["isError"], errors="coerce").fillna(0)
df["gasUsed"] = pd.to_numeric(df["gasUsed"], errors="coerce").fillna(0)

# === Step 4: Score Assignment ===
wallet_scores = []

print("\n🚀 Assigning scores based on transaction data...")

for wallet_id, group in tqdm(df.groupby("wallet_id")):
    txn_count = len(group)
    total_value = group["value"].sum() / 1e18
    avg_value = group["value"].mean() / 1e18
    unique_recipients = group["to"].nunique()
    unique_methods = group["methodId"].nunique()
    failed_txns = group["isError"].sum()
    success_rate = (txn_count - failed_txns) / txn_count if txn_count else 0

    score = 0
    score += min(np.log1p(txn_count) * 60, 200)
    score += min(np.sqrt(total_value) * 40, 200)
    score += min(unique_recipients * 4, 100)
    score += min(unique_methods * 6, 100)
    score += min(np.log1p(avg_value) * 60, 200)
    score += success_rate * 200

    score = max(0, min(int(round(score)), 1000))
    wallet_scores.append({"wallet_id": wallet_id, "score": score})

# === Step 5: De-cluster Scores (small perturbation) ===
df_scores = pd.DataFrame(wallet_scores)

# Count how many times each score occurs
score_counts = df_scores["score"].value_counts()

# Prepare a mapping to track how many have been adjusted
adjustment_counter = defaultdict(int)

for idx, row in df_scores.iterrows():
    current_score = row["score"]
    count = score_counts[current_score]

    if count > 3:
        n = adjustment_counter[current_score]
        new_score = current_score + (-1)**n * ((n + 1) // 2)  # Apply ±1, ±2, ...
        new_score = max(0, min(1000, new_score))
        df_scores.at[idx, "score"] = new_score
        adjustment_counter[current_score] += 1

# === Step 6: Save Output ===
df_scores[["wallet_id", "score"]].to_csv(OUTPUT_PATH, index=False)

# === Step 7: Summary and Health Check ===
print("\n📊 Final Score Range Distribution:")
bins = [0, 200, 400, 600, 800, 1000]
labels = ["0–200", "200–400", "400–600", "600–800", "800–1000"]
df_scores["score_bucket"] = pd.cut(df_scores["score"], bins=bins, labels=labels, include_lowest=True)
print(df_scores["score_bucket"].value_counts().sort_index())

print("\n🔍 Quality Check:")
print(f"Total wallets: {len(df_scores)}")
print(f"Missing values: \n{df_scores.isnull().sum()}")
print(f"Duplicate wallet_ids: {df_scores['wallet_id'].duplicated().sum()}")

# === Final Check for Repetitions ===
repeat_check = df_scores["score"].value_counts()
print("\n🚨 Scores repeated more than 3 times:")
print(repeat_check[repeat_check > 3])

print("\n✅ Final version saved to:")
print(OUTPUT_PATH)