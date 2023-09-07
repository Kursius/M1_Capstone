import re

def is_valid_password(password):
    # Define the regular expression pattern
    pattern = r'^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=!?]).{8,}$'
    
    # Use re.search to check if the password matches the pattern
    if re.search(pattern, password):
        return True
    else:
        return False

# Test cases
password1 = "Vidaslopas1?"
password2 = "weakpass"
print(is_valid_password(password1))  # True (meets requirements)
print(is_valid_password(password2))  # False (does not meet requirements)
