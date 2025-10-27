import base64
import hashlib
import time

# --- CONFIDENTIALITY ---
def confidentiality(message):
    print("\n--- CONFIDENTIALITY ---")
    print("Original Message:", message)
    
    # Encrypt using Base64
    encrypted = base64.b64encode(message.encode("utf-8")).decode("utf-8")
    print("Encrypted Message:", encrypted)
    
    # Decrypt back
    decrypted = base64.b64decode(encrypted.encode("utf-8")).decode("utf-8")
    print("Decrypted Message:", decrypted)


# --- INTEGRITY ---
def integrity(data):
    print("\n--- INTEGRITY ---")
    print("Original Data:", data)
    
    # Hash of original data
    hash1 = hashlib.sha256(data.encode("utf-8")).hexdigest()
    print("Hash of Original Data:", hash1)
    
    # Modify data slightly
    modified_data = data + "s"
    print("Modified Data:", modified_data)
    hash2 = hashlib.sha256(modified_data.encode("utf-8")).hexdigest()
    print("Hash of Modified Data:", hash2)


# --- AVAILABILITY ---
def availability():
    print("\n--- AVAILABILITY ---")
    print("Service Status: Available ✅")
    time.sleep(1)  # simulate normal running
    
    print("Simulating attack...")
    time.sleep(1)
    print("Service Status: Unavailable ❌")


# MAIN PROGRAM
if __name__ == "__main__":
    # Run with first message
    confidentiality("This is a secret message: Do not share Prateek!")
    integrity("Important transaction record")
    availability()

    print("\n" + "="*60 + "\n")
    
    # Run with second message (only message changed)
    