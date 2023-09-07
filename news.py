# implement user registration system to .json files

import json
from dataclasses import dataclass
import re


# class to store user data(username, email, password)
@dataclass
class User:
    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def setUsername(self, username):
        # check if username is already taken by reading .json file with username as filename
        try:
            with open(username + ".json", "r") as file:
                print("Username already taken. Please select a diffrent username.")
                return False
        except FileNotFoundError:
            self.username = username
            return True

    def setEmail(self, email):
        # with regular expressions, check if email is valid (contains @, etc.)
        if re.match(
            r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=.{8,})", email
        ):
            self.email = email
            return True
        else:
            print("Invalid email address.")
            return False

    def setPassword(self, password):
        # with regex, check if password is valid (contains at least 1 number, 1 uppercase, 1 lowercase, 1 special character, and is at least 8 characters long)
        if re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]", password
        ):
            self.password = password
            return True
        else:
            print(
                "Invalid password. Password must use: 1 number, 1 uppercase, 1 lowercase, 1 special character and be at least 8 characters long."
            )
            return False


# using User class to create a new user
def createUser():
    user = User()
    while True:
        username = input("Enter your username: ")
        if user.setUsername(username):
            break
        else:
            continue

    while True:
        email = input("Enter your email: ")
        if user.setEmail(email):
            break
        else:
            continue

    while True:
        password = input(
            "Enter a password. Password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 special character: "
        )
        if user.setPassword(password):
            break
        else:
            continue

    # store user data in individual .json file with username as filename
    username.json = {"username": username, "email": email, "password": password}
    with open(username + ".json", "w") as file:
        json.dump(username.json, file)


# menu function to manage options to user (login, register, exit)
def menu():
    print("Welcome to the News API!")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    choice = input("Enter your choice: ")
    return choice

def main():
    while True:
        #menu fuctionality with case-match to call functions
        choice = menu()
        match choice:
            case "1":
                print("Login")
            case "2":
                createUser()
            case "3":
                print("Goodbye!")
                exit()
            case _:
                print("Invalid choice. Please try again.")
                continue   