# IP Geolocation Console Application

## Description
This is a console-based Python application that combines secure user authentication and IP geolocation functionalities. It provides features such as:

- User registration with secure password hashing.
- CAPTCHA verification for enhanced security.
- Login with limited attempts to prevent brute force attacks.
- Password recovery using security questions.
- IP Geolocation lookup using a public API.

## Features
1. **User Registration**
   - Captures user email, password, and a security question.
   - Validates email and password for security and format.
   - Passwords are hashed using `bcrypt` for secure storage.
   - Stores user details in a CSV file (`Your_DataBase.csv`).

2. **User Login**
   - Validates credentials against stored values in the database.
   - Includes CAPTCHA verification and limits to 5 login attempts.
   - If login is successful, the user can fetch IP geolocation data.

3. **Forgot Password**
   - Prompts the user to answer their security question to reset their password.
   - Ensures the new password meets security criteria and is different from the old password.

4. **IP Geolocation**
   - Uses the `ip-api.com` API to retrieve geolocation information such as country, city, region, and timezone.
   - Allows users to input a specific IP address or use their own.

## Prerequisites
- Python 3.6 or higher
- `bcrypt` library for password hashing
- `requests` library for API interaction

Install dependencies using:
```bash
pip install bcrypt requests
```

## How to Run the Application
1. Clone this repository.
2. Run the script using:
   ```bash
   python app.py
   ```
3. Follow the on-screen instructions to register, log in, or recover your password.

## File Structure
- `app.py`: Main application file containing all functionality.
- `Your_DataBase.csv`: Automatically created CSV file to store user credentials and security questions.

## CSV Database
- The application will create a file named `Your_DataBase.csv` in the working directory.
- This file stores the following fields for each user:
  - **Email**: User's email address.
  - **Hashed Password**: Securely hashed password.
  - **Security Question**: User-provided question for password recovery.

## Security Features
- Passwords are securely hashed using the `bcrypt` library.
- CAPTCHA verification prevents automated abuse.
- Password recovery is secured by a user-defined security question.
- Ensures strong password requirements (minimum 8 characters, mix of uppercase, lowercase, digits, and special characters).

## Example Usage
1. **Registration**:
   - User enters their email, password, and security question.
   - Validations ensure proper email format and strong password.
2. **Login**:
   - User provides their email and password.
   - If credentials match, the user is authenticated.
3. **Forgot Password**:
   - User answers the security question to reset their password.
   - Validations ensure the new password meets security requirements.
4. **IP Geolocation**:
   - User can provide an IP address or use their own to fetch geolocation details.

## API Usage
This application utilizes the `ip-api.com` API for IP geolocation services. Make sure you have an active internet connection to fetch geolocation details.

## Screenshots
- Coming soon!

## License
This project is licensed under the MIT License.

---

Feel free to modify this README file to better suit your needs or add more specific instructions!
