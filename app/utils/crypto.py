import os
import base64

def hash_password(password):
    """
    Return the password as plaintext (no hashing).
    
    Args:
        password (str): The password.
    
    Returns:
        str: The plaintext password.
    """
    # Just return the password as is (plaintext)
    return password

def verify_password(password, stored_password):
    """
    Verify a password against a stored password (plaintext comparison).
    
    Args:
        password (str): The password to verify.
        stored_password (str): The stored password to check against.
    
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    # Simple string comparison
    return password == stored_password

def generate_token(length=32):
    """
    Generate a random token for use in secure operations.
    
    Args:
        length (int, optional): The length of the token in bytes. Defaults to 32.
    
    Returns:
        str: A random token encoded as a base64 string.
    """
    # Generate random bytes
    token_bytes = os.urandom(length)
    
    # Encode as base64 and return as string
    token = base64.urlsafe_b64encode(token_bytes).decode('utf-8')
    return token.rstrip('=')  # Remove padding characters

if __name__ == "__main__":
    # Test the password handling and verification
    password = "test_password"
    stored = hash_password(password)
    print(f"Original password: {password}")
    print(f"Stored password: {stored}")
    
    # Verify the password
    is_valid = verify_password(password, stored)
    print(f"Password verification: {is_valid}")
    
    # Test with wrong password
    wrong_password = "wrong_password"
    is_valid = verify_password(wrong_password, stored)
    print(f"Wrong password verification: {is_valid}")
    
    # Generate a token
    token = generate_token()
    print(f"Generated token: {token}")