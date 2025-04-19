import tenseal as ts

def generate_context():
    # Create a BFV context
    context = ts.context(
        ts.SCHEME_TYPE.BFV,
        poly_modulus_degree=8192,
        plain_modulus=1032193  # ⚠️ Must match DB encryption
    )
    context.generate_galois_keys()  # Generate keys for rotation
    context.generate_relin_keys()  # Generate keys for relinearization

    # Save the context with the secret key
    with open("tenseal_context_bfv.pkl", "wb") as f:
        f.write(context.serialize(save_secret_key=True))  # Secret key saved here for query encryption

    print("✅ BFV context generated and saved as 'tenseal_context_bfv.pkl'")

if __name__ == "__main__":
    generate_context()
