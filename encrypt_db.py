import os
import psycopg2
from dotenv import load_dotenv
import tenseal
import psycopg2.extras

# Load environment variables
load_dotenv()

def connect_postgres(dbname):
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", 5432))
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "Suman@1630")

    print(f"Connecting to {dbname} as {user}...")

    if not password:
        print("ERROR: No password provided in .env file!")
        return None

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        print(f"Connected to {dbname} successfully.")
        return conn
    except Exception as e:
        print(f"❌ Connection error for {dbname}:", e)
        return None

def init_tenseal_context(save_path="bfv_context.ctx"):
    """
    Initialize and save a TenSEAL BFV context with secret key.
    """
    context = tenseal.context(
        tenseal.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193
    )
    context.generate_galois_keys()
    context.generate_relin_keys()
    
    # Save context with secret key
    with open(save_path, "wb") as f:
        f.write(context.serialize(save_secret_key=True))
        print(f"🔐 BFV context saved to {save_path}")
    
    return context

def encrypt_integer(context, value):
    """
    Encrypts a valid integer using BFV and returns serialized ciphertext.
    """
    try:
        int_value = int(value)
        encrypted_vector = tenseal.bfv_vector(context, [int_value])
        return encrypted_vector.serialize()
    except Exception as e:
        print(f"⚠ Error encrypting value '{value}':", e)
        return None

def update_encrypted_columns(conn, report_number, rn_enc, crime_code_enc, victim_age_enc):
    """
    Update the encrypted fields in the crime_data table.
    """
    query = """
        UPDATE crime_data
        SET report_number_enc = %s,
            crime_code_enc = %s,
            victim_age_enc = %s
        WHERE report_number = %s;
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (
                psycopg2.Binary(rn_enc),
                psycopg2.Binary(crime_code_enc),
                psycopg2.Binary(victim_age_enc),
                report_number
            ))
        conn.commit()
    except Exception as e:
        print(f"❌ Error updating row with report_number {report_number}:", e)

def process_database(dbname, context):
    """
    Encrypt and store selected columns for all rows in the specified database.
    """
    conn = connect_postgres(dbname)
    if conn is None:
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT report_number, crime_code, victim_age FROM crime_data;")
            rows = cursor.fetchall()
    except Exception as e:
        print(f"❌ Error fetching data from {dbname}:", e)
        conn.close()
        return

    print(f"🔄 Encrypting {len(rows)} rows in {dbname}...")

    for row in rows:
        report_number, crime_code, victim_age = row

        # Skip rows with invalid values
        if any(v is None for v in [report_number, crime_code, victim_age]):
            print(f"⚠ Skipping row with null values: {row}")
            continue

        try:
            rn_enc = encrypt_integer(context, report_number)
            code_enc = encrypt_integer(context, crime_code)
            age_enc = encrypt_integer(context, victim_age)

            if rn_enc and code_enc and age_enc:
                update_encrypted_columns(conn, report_number, rn_enc, code_enc, age_enc)
            else:
                print(f"⚠ Skipping row {report_number} due to encryption error.")
        except Exception as e:
            print(f"❌ Unexpected error for row {report_number}:", e)

    print(f"✅ Done encrypting {dbname}.")
    conn.close()

def main():
    databases = ["delhi_crime_db", "mumbai_crime_db"]
    context = init_tenseal_context()

    for dbname in databases:
        process_database(dbname, context)

if __name__ == "__main__":
    main()
