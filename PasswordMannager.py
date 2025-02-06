from cryptography.fernet import Fernet
import os

# Function to generate and save a key if it doesn't exist
def write_key():
    if not os.path.exists("key.key"):  # Check if key file exists
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        print("Encryption key generated and saved as 'key.key'.")

# Function to load the encryption key
def load_key():
    with open("key.key", "rb") as key_file:
        return key_file.read()

# Ensure key exists before loading
write_key()
key = load_key()
fer = Fernet(key)

# Function to view stored passwords
def view():
    if not os.path.exists("passwords.txt"):
        print("No saved passwords found.")
        return
    
    with open('passwords.txt', 'r') as f:
        for line in f:
            data = line.strip()
            if "|" in data:
                user, passw = data.split("|")
                try:
                    decrypted_pass = fer.decrypt(passw.encode()).decode()
                    print(f"User: {user} | Password: {decrypted_pass}")
                except Exception as e:
                    print(f"Error decrypting password for {user}: {e}")

# Function to add new passwords
def add():
    name = input('Account Name: ').strip()
    pwd = input("Password: ").strip()
    
    if not name or not pwd:
        print("Account name and password cannot be empty.")
        return
    
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()
    
    with open('passwords.txt', 'a') as f:
        f.write(f"{name}|{encrypted_pwd}\n")

# Main loop
while True:
    mode = input("Would you like to add a new password or view existing ones (view, add)? Press q to quit: ").lower()
    
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode. Please enter 'view', 'add', or 'q' to quit.")
