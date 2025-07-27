import os
import time
import json
import requests
import pandas as pd
from tqdm import tqdm

# === CONFIG ===
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # ✅ Now fetched from environment variable
WALLET_CSV_PATH = "../data/Wallet id - Sheet1.csv"
OUTPUT_JSON_PATH = "../output/wallet_transactions.json"
MAX_TXNS_PER_WALLET = 10000

# === LOAD WALLETS ===
wallet_df = pd.read_csv(WALLET_CSV_PATH)
wallet_list = wallet_df.iloc[:, 0].dropna().unique().tolist()

print(f"🔍 Total wallets loaded: {len(wallet_list)}")

# === Etherscan API URL ===
BASE_URL = "https://api.etherscan.io/api"

# === FINAL OUTPUT ===
wallet_data = {}

# === FETCH TRANSACTIONS ===
def fetch_wallet_transactions(wallet):
    try:
        params = {
            "module": "account",
            "action": "txlist",
            "address": wallet,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc",
            "apikey": ETHERSCAN_API_KEY  # ✅ Uses env variable
        }
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if data["status"] == "1" and "result" in data:
            return data["result"]
        else:
            return []
    except Exception as e:
        print(f"❌ Error for {wallet[:8]}...: {e}")
        return []

# === MAIN LOOP ===
for idx, wallet in enumerate(tqdm(wallet_list, desc="🔄 Fetching Transactions")):
    transactions = fetch_wallet_transactions(wallet)
    wallet_data[wallet] = transactions

    print(f"[{idx + 1}/{len(wallet_list)}] Wallet: {wallet}")
    print(f"✅ Fetched {len(transactions)} transactions.")

    time.sleep(0.25)

    if (idx + 1) % 5 == 0:
        with open(OUTPUT_JSON_PATH, "w") as f:
            json.dump(wallet_data, f, indent=2)
        print(f"💾 Autosaved {idx + 1} records...")

# === FINAL SAVE ===
with open(OUTPUT_JSON_PATH, "w") as f:
    json.dump(wallet_data, f, indent=2)

print("\n✅ All transactions fetched and saved successfully.")
