import random
import string
import hashlib
import sqlite3

def generate_password():
    # Define the character set for the password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate a random password
    password = ''.join(random.choice(characters) for i in range(12))
    
    # Return the password
    return password

# Connect to the database
conn = sqlite3.connect('passwords.db')

# Create a table for the passwords if it doesn't already exist
conn.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY,
             hashed_password TEXT,
             plaintext_password TEXT);''')

# Check if there are any passwords stored in the database
cursor = conn.execute("SELECT hashed_password FROM passwords;")
hashed_passwords = [row[0] for row in cursor]
if not hashed_passwords:
    # Prompt the user to set a master password
    master_password = input('Set a master password: ')
    
    # Hash the master password and insert it into the database
    hashed_master_password = hashlib.sha256(master_password.encode()).hexdigest()
    conn.execute("INSERT INTO passwords (hashed_password, plaintext_password) VALUES (?, ?);", (hashed_master_password, None))
    print('Master password set')
    
    # Commit the changes to the database
    conn.commit()

def check_password():
    print("=" * 52)
    print("||{:^48}||".format("PyVault"))
    print("=" * 52)
    # Prompt the user to enter the master password
    master_password = input('Enter master password: ')
    
    # Hash the entered password and compare it with the stored hash
    hashed_master_password = hashlib.sha256(master_password.encode()).hexdigest()
    
    # Retrieve the hashed master password from the database
    cursor = conn.execute("SELECT hashed_password FROM passwords;")
    hashed_passwords = [row[0] for row in cursor]
    
    # Check if the entered password matches any of the stored hashes
    if hashed_master_password in hashed_passwords:
        while True:
            # Prompt the user to choose an action
            action = input('Enter "1" to view saved passwords, "2" to generate a new password, or "q" to quit: ')
            
            if action == '1':
                # Retrieve all the saved passwords from the database
                cursor = conn.execute("SELECT id, plaintext_password FROM passwords;")
                passwords = {row[0]: row[1] for row in cursor}
                
                # Print the passwords
                for id, password in passwords.items():
                    print(f'{id}: {password}')
                
            elif action == '2':
                # Generate a new password
                password = generate_password()
                
                # Hash the password and insert it into the database
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                conn.execute("INSERT INTO passwords (hashed_password, plaintext_password) VALUES (?, ?);", (hashed_password, password))
                print('New password generated:', password)
                
                # Commit the changes to the database
                conn.commit()
                
            elif action == 'q':
                break
                
            else:
                print('Invalid action')
                
    else:
        print('Invalid password')

# Call the check_password function to start the program
check_password()

# Close the connection to the database
conn.close()
