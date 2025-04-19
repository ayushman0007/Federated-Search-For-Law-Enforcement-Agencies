# 🛡️ Secure Federated Search for Law Enforcement Agencies using Homomorphic Encryption & Blockchain

This project implements a secure, privacy-preserving crime data query system across multiple cities (Mumbai & Delhi) using **Homomorphic Encryption (BFV)**, **Federated Search**, **OAuth2 Authentication**, and **Blockchain Logging**.

---

## 🚀 Features

- 🔐 **BFV Homomorphic Encryption** using TenSEAL for searchable encrypted fields.
- 🏙️ **Federated search** across multiple PostgreSQL databases (Mumbai & Delhi).
- 🔎 **Encrypted query matching** on `report_number` with no data leakage.
- ⛓️ **Blockchain ledger** to record all search activity for audit trails.
- 🔏 **Zero Knowledge Proof simulation** to verify access without revealing data.
- 🔑 **OAuth2 Token Authentication** (mock server + client app).
- 🧹 **Preprocessing** and context generation for secure encryption workflows.

---

## 🛠️ Technologies Used

| Category         | Tool/Library              |
|------------------|---------------------------|
| Programming      | Python 3.10+              |
| Database         | PostgreSQL                |
| Encryption       | TenSEAL (BFV Scheme)      |
| Auth Simulation  | Flask, OAuth2             |
| Blockchain       | Custom JSON ledger        |
| Env Management   | python-dotenv             |

---


## 🧪 Setup Instructions

### ✅ 1. Clone the Repo and Install Requirements

```bash
git clone https://github.com/your-username/FederatedSearchForLawEnforcementAgencie.git
cd crime-encryption-search
pip install -r requirements.txt
```
### ✅ 3. Set Up PostgreSQL Databases
Create two databases:
```bash
createdb mumbai_crime_db
createdb delhi_crime_db
```
### ✅ 4. Add Environment Variables
Create a .env file: 
```bash
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
MUMBAI_DB=mumbai_crime_db
DELHI_DB=delhi_crime_db
```

## 🔐 Encryption & Storage
### Step 1: Generate BFV Encryption Context
```bash
python generate_bfv_context.py
```
### Step 2: Encrypt Crime Data and Store in DB
```bash
python encrypt_db.py
```
This script loads raw data from delhi_crime_data_modified.py and mumbai_crime_data_modified.py, encrypts sensitive fields, and saves them (both plaintext and encrypted) to PostgreSQL.

## 🔍 Encrypted Federated Search
Run:
```bash
python clean_preprocessdata.py
```
This will:
- Ask for a report number
- Encrypt it using BFV
- Search both Delhi and Mumbai databases
- Match encrypted values securely
- Simulate a ZKP-based verification
- Append the search to search_blockchain.json

## 🔒 OAuth2 Authentication (Mock)
### ▶️ Start the Auth Server
```bash
python auth_server.py
```
### ▶️ Start the Client App
```bash
python client_app.py
```
This will simulate the OAuth2 flow using client_secrets.json. After authentication, an access token will be issued and printed.
## 👤 Author
Sakshi (22BIT0515)

Ayushman Singh (22BIT0473)
