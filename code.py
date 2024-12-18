import csv
import bcrypt
import re
import requests
import random
import string
import os

os.system('cls')

USER_DB = 'Your_DataBase.csv'

def is_valid_email(email):
    return "@" in email and "." in email

def is_valid_password(password):
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(char in '!@#$%^&*' for char in password)
    
    return len(password) >= 8 and has_upper and has_lower and has_digit and has_special

def generate_captcha():
    """Generates a random 6-character CAPTCHA."""
    characters = string.ascii_letters + string.digits  # Letters and digits
    captcha = ''.join(random.choice(characters) for i in range(6))
    return captcha

def verify_captcha():
    """Prompts the user to input the CAPTCHA."""
    captcha = generate_captcha()
    print(f"CAPTCHA: {captcha}")
    user_input = input("Enter the CAPTCHA: ")
    return user_input == captcha

def is_email_exist(email):
    """Check if the email already exists in the database."""
    try:
        with open(USER_DB, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:  # Compare with the email in the CSV
                    return True
    except FileNotFoundError:
        # If the file does not exist, that means no users are registered yet
        return False
    return False

def register_user():
    # CAPTCHA verification before registration
    if not verify_captcha():
        print("CAPTCHA verification failed. Please try again.")
        return
    
    email = input("Enter your email: ")
    
    # Check if email already exists in the database
    if is_email_exist(email):
        print("This email is already registered. Please use a different email.")
        return
    
    if not is_valid_email(email):
        print("Invalid email format.")
        return
    
    password = input("Enter your password: ").encode('utf-8')
    if not is_valid_password(password.decode('utf-8')):
        print("Password must be at least 8 characters long, contain uppercase, lowercase, a number, and a special character.")
        return
    
    security_question = input("Enter your security question for password recovery: ")
  
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Save the new user to the CSV file
    with open(USER_DB, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password.decode('utf-8'), security_question])
    
    print("User registered successfully.")

    
def login_user():
    # CAPTCHA verification before login
    if not verify_captcha():
        print("CAPTCHA verification failed. Please try again.")
        return False
    
    attempts = 5
    while attempts > 0:
        email = input("Enter your email: ")
        password = input("Enter your password: ").encode('utf-8')

        with open(USER_DB, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                stored_email, stored_hashed_password, _ = row
                if email == stored_email:
                    if bcrypt.checkpw(password, stored_hashed_password.encode('utf-8')):
                        print("Login successful!")
                        return True
                    else:
                        print("Incorrect password.")
                        attempts -= 1
                        print(f"{attempts} attempts remaining.")
                        break
            else:
                print("Email not found.")
                attempts -= 1
                print(f"{attempts} attempts remaining.")
                
        if attempts == 0:
            print("Too many failed attempts. Access blocked.")
            return False

def forgot_password():
    # CAPTCHA verification before password reset
    if not verify_captcha():
        print("CAPTCHA verification failed. Please try again.")
        return
    
    email = input("Enter your registered email: ")
   
    with open(USER_DB, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            stored_email, stored_hashed_password, stored_security_question = row
            if email == stored_email:
                print(f"Security Question: {stored_security_question}")
                answer = input("Answer: ")
                
                if answer:
                    while True:
                        new_password = input("Enter your new password: ")
                        if not is_valid_password(new_password):
                            print("New password does not meet criteria. Please try again.")
                            continue

                        
                        if bcrypt.checkpw(new_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                            print("New password cannot be the same as the old password. Please try a different password.")
                        else:
                            
                            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                            update_user_password(email, hashed_password.decode('utf-8'))
                            print("Password reset successfully.")
                            return
    print("Email not found or incorrect answer.")

    
def update_user_password(email, new_hashed_password):
    rows = []
    
    with open(USER_DB, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    with open(USER_DB, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == email:
                row[1] = new_hashed_password
            writer.writerow(row)

def get_geolocation(ip=""):
    if not ip:
        ip = requests.get("https://api.ipify.org").text
    
    response = requests.get(f"http://ip-api.com/json/{ip}")
    
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'success':
            print(f"IP: {data['query']}")
            print(f"Country: {data['country']}")
            print(f"City: {data['city']}")
            print(f"Region: {data['regionName']}")
            print(f"Latitude: {data['lat']}")
            print(f"Longitude: {data['lon']}")
            print(f"Timezone: {data['timezone']}")
            print(f"ISP: {data['isp']}")
        else:
            print("Error: Invalid IP address.")
    else:
        print("Error: Unable to reach the API.")

def main_menu():
    while True:
        print("\n" + "=" * 156)
        print("\t\t\t\t\t\t✨ Welcome to the IP Geolocation Application ✨")
        print("=" * 156)
        print("\n\tPlease select an option from the menu below:")
        
        print("\n\t[1] 👤 Register")
        print("\t[2] 🔐 Login")
        print("\t[3] ❓ Forgot Password")
        print("\t[4] 🚪 Quit\n")

        print("=" * 156)
        choice = input("\n\t🔍 Enter your choice: ")

        if choice == '1':
            print("\n📝 Registering a new user...")
            register_user()
        elif choice == '2':
            print("\n🔑 Login Process...")
            if login_user():
                ip = input("\n📡 Enter an IP address (leave blank to use your own IP): ")
                get_geolocation(ip)
        elif choice == '3':
            print("\n🔐 Password Recovery...")
            forgot_password()
        elif choice == '4':
            print("\n👋 Thank you for using the IP Geolocation Application! Goodbye!")
            break
        else:
            print("\n⚠️ Invalid option. Please try again.")
        
        input("\n🔄 Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
