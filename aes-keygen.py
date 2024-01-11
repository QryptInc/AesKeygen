import requests
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import csv

api_token = "Your API token here"
out_file = "outfile.csv"
key_size = 32
iv_size = 16
test_keys = True  # You can set this to False if you don't want to test keys

# Perform API request to get quantum entropy
response = requests.get("https://api-eus.qrypt.com/api/v1/quantum-entropy?size=100", headers={"Authorization": f"Bearer {api_token}"})
data = response.json()

# Create a list to store key-IV pairs
key_iv_pairs = []

# Process quantum entropy data
for i in range(0, len(data['random']), key_size * 2 + iv_size * 2):  # Account for hexadecimal representation
    key_offset = i
    iv_offset = i + key_size * 2

    aes_key_hex = ''.join(data['random'][key_offset:key_offset + key_size * 2])
    aes_iv_hex = ''.join(data['random'][iv_offset:iv_offset + iv_size * 2])

    # Remove non-hexadecimal characters from the key and IV
    aes_key_hex = ''.join(c for c in aes_key_hex if c in '0123456789abcdefABCDEF')
    aes_iv_hex = ''.join(c for c in aes_iv_hex if c in '0123456789abcdefABCDEF')

    # Ensure the AES key is 256 bits (32 bytes) by generating a random key if needed
    if len(aes_key_hex) != key_size * 2:
        aes_key = get_random_bytes(key_size)
    else:
        aes_key = bytes.fromhex(aes_key_hex)

    # Ensure the IV is the correct length, generate random IV if needed
    if len(aes_iv_hex) != iv_size * 2:
        aes_iv = get_random_bytes(iv_size)
    else:
        aes_iv = bytes.fromhex(aes_iv_hex)

    key_iv_pairs.append((aes_key.hex(), aes_iv.hex()))

# Test keys
if test_keys:
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
    plaintext = b'test data'
    
    # Padding the plaintext to be a multiple of 16 bytes
    padded_plaintext = pad(plaintext, AES.block_size)

    ciphertext = cipher.encrypt(padded_plaintext)

    # Create a new cipher object for decryption
    decipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
    decrypted_padded = decipher.decrypt(ciphertext)

    # Unpad the decrypted text
    decrypted = unpad(decrypted_padded, AES.block_size)

    if decrypted != plaintext:
        print("Key test failed!")

# Write key-IV pairs to a CSV file
with open(out_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["KEY", "IV"])
    csvwriter.writerows(key_iv_pairs)

print('Success!')
print(f'Wrote {len(key_iv_pairs)} key-IV pairs to {out_file}')
