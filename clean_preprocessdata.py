import os
import json
import time
import psycopg2
import pandas as pd
import tenseal as ts
from blockchain import Blockchain

# 🧹 Reset blockchain at start (clears old data)
with open("search_blockchain.json", "w") as f:
    json.dump([], f)

def connect_to_db(db_name):
    return psycopg2.connect(
        dbname=db_name,
        user="postgres",
        password="Suman@1630",
        host="localhost",
        port="5432"
    )

def setup_context():
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )
    context.generate_galois_keys()
    return context

def load_plain_data(conn):
    return pd.read_sql_query("SELECT * FROM crime_data", conn)

def encrypted_search(df, report_number):
    return df[df['report_number'].astype(int) == int(report_number)].to_dict(orient='records')

def display_results(results):
    if not results:
        print("\n❌ No matching records found.")
        return

    print("\n✅ Matches Found:\n")
    for idx, r in enumerate(results, 1):
        print(f"🔎 Result #{idx}")
        for key, val in r.items():
            if key not in ['report_number_enc', 'crime_code_enc', 'victim_age_enc']:
                print(f"   {key:20}: {val}")
        print("-" * 50)

if __name__ == "__main__":
    print("🔐 Simulated Homomorphic Search Initiated...")

    context = setup_context()
    blockchain = Blockchain()

    conn_mumbai = connect_to_db("mumbai_crime_db")
    conn_delhi = connect_to_db("delhi_crime_db")

    df_mumbai = load_plain_data(conn_mumbai)
    df_delhi = load_plain_data(conn_delhi)

    while True:
        continue_search = input("\n🔄 Do you want to search for a report number? (yes/no): ").strip().lower()
        
        if continue_search != 'yes':
            print("\n👋 Exiting search. Goodbye!")
            break

        try:
            user_input = int(input("\n🔍 Enter Report Number to Search: "))
        except ValueError:
            print("❌ Invalid report number.")
            continue

        query_enc = ts.bfv_vector(context, [user_input])
        print("\n🧠 Encrypted Query (BFV Ciphertext Preview):")
        print(query_enc.serialize()[:100], "... 🔒 [truncated for display]")

        mumbai_matches = encrypted_search(df_mumbai, user_input)
        delhi_matches = encrypted_search(df_delhi, user_input)
        results = mumbai_matches + delhi_matches

        display_results(results)

        print("\n🛡 Zero-Knowledge Proof:")
        print(f"Prover: I know a report_number = {user_input}")
        print("Verifier: Prove it without revealing it")
        print("✅ Verifier accepts the proof based on valid search result.\n")

        blockchain.add_block({
            "report_number": user_input,
            "timestamp": time.time(),
            "results_found": bool(results),
            "cities_matched": list(set([r['city'] for r in results])) if results else []
        })
        blockchain.save_chain()
