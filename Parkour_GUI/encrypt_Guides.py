from cryptography.fernet import Fernet

KEY_FILE = "parkour.key"
INPUT_FILE = "guides.json"
OUTPUT_FILE = "guides.enc"

key = Fernet.generate_key()

with open(KEY_FILE, "wb") as file:
    file.write(key)

with open(INPUT_FILE, "rb") as file:
    guide_data = file.read()

encrypted_data = Fernet(key).encrypt(guide_data)

with open(OUTPUT_FILE, "wb") as file:
    file.write(encrypted_data)

print("Created guides.enc")
print("Keep parkour.key safe. You need it to decrypt the guides.")
