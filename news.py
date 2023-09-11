import json
from dataclasses import dataclass
import re
import ssl
import smtplib
import requests
from email.message import EmailMessage
import random
import os

API_WEATHER = os.environ.get("API_WEATHER")
API_NEWS = os.environ.get("API_NEWS")
EMAIL_SENDER = os.environ.get("EMAIL_SENDER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")


# class to store user data(username, email, password)
@dataclass
class User:
    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password
    
    #setters
    def setUsername(self, username):
        # check if username is already taken by reading .json file with username as filename
        try:
            with open(username + ".json", "r") as file:
                print("\033[31mUsername already taken. Please select a diffrent username.\033[0m")
                print("")
                return False
        except FileNotFoundError:
            self.username = username
            return True

    def setEmail(self, email):
        # with regular expressions, check if email is valid (contains @, etc.)
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            self.email = email
            return True
        else:
            print("\033[31mInvalid email address.\033[0m")
            return False

    def setPassword(self, password):
        # with regex, check if password is valid (contains at least 1 number, 1 uppercase, 1 lowercase, 1 special character, and is at least 8 characters long)
        if re.match(
            r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$%^&+=!?]).{8,}$", password
        ):
            self.password = password
            return True
        else:
            print("\033[31mInvalid password.\033[0m")
            return False

    def getEmail(self):
        return self.email
    
    #methods
    def changePassword(self) -> None:
        currentPassword = input("Enter your current password: ")
        if currentPassword == self.password:
            while True:
                password = input(
                    "Enter a password. Password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 special character: "
                )
                if self.setPassword(password):
                    break
                else:
                    continue
            updateUser(self)
            print("\033[32mPassword changed successfully!\033[0m")
        else:
            print("\033[31mIncorrect password. Please try again.\033[0m")

    
    def updateUser(self):
        with open(self.username + ".json", "w") as file:
            json.dump(
                {
                    "username": self.username,
                    "email": self.email,
                    "password": self.password,
                },
                file,
                indent=4,
            )

def getWeather(user: User) -> None:
    # get weather data from API
    apiKey = API_WEATHER
    location = input("Enter location: ")
    timeframe = input("Enter the forecast timeframe (1-7 days): ")
    url = f"https://api.weatherapi.com/v1/forecast.json?key={apiKey}&q={location}&days={timeframe}"
    response = requests.get(url)
    data = response.json()
    # if location is not found, user is asked to try again
    if "error" in data:
        print("\033[31mLocation not found. Please try again.\033[0m")
        return
    # if location is found, weather data is printed
    else:
        # generate an email body with weather data for location, then send user and email body to sendEmail function
        body = ""
        body += f"Weather for {location}:\n\n"
        for i in range(int(timeframe)):
            body += f"Date: {data['forecast']['forecastday'][i]['date']}\n"
            body += f"Max temperature: {data['forecast']['forecastday'][i]['day']['maxtemp_c']}°C\n"
            body += f"Min temperature: {data['forecast']['forecastday'][i]['day']['mintemp_c']}°C\n"
            body += f"Average temperature: {data['forecast']['forecastday'][i]['day']['avgtemp_c']}°C\n"
            body += f"Max wind speed: {data['forecast']['forecastday'][i]['day']['maxwind_kph']}kph\n"
            body += f"Total precipitation: {data['forecast']['forecastday'][i]['day']['totalprecip_mm']}mm\n"
            body += f"Average humidity: {data['forecast']['forecastday'][i]['day']['avghumidity']}%\n"
            body += f"Chance of rain: {data['forecast']['forecastday'][i]['day']['daily_chance_of_rain']}%\n"
            body += f"Chance of snow: {data['forecast']['forecastday'][i]['day']['daily_chance_of_snow']}%\n"
            body += "\n"
        sendEmail(user, body)
        print("\033[32mWeather forecast sent to your email address.\033[0m")


# function to get news data from API by category, that user can enter, and the amount of articles, that user can enter
def getNews(user : User) -> None:
    apiKey = API_NEWS
    category = input("Enter news category: ")
    amount = input("Enter the amount of articles (1-10): ")
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={apiKey}&pageSize={amount}"
    response = requests.get(url)
    data = response.json()
    # if category is not found, user is asked to try again
    if data["totalResults"] == 0:
        print("\033[31mCategory not found. Please try again.\033[0m")
        return
    # if category is found, news data is printed

    else:
        # generate an email body with news data for each article, then send user and email body to sendEmail function
        body = ""
        body += f"News for {category}:\n\n"
        for i in range(int(amount)):
            body += f"Title: {data['articles'][i]['title']}\n"
            body += f"Description: {data['articles'][i]['description']}\n"
            body += f"Link: {data['articles'][i]['url']}\n"
            body += "\n"
        sendEmail(user, body)
        print("\033[32mNews sent to your email address.\033[0m")


# using User class to create a new user
def createUser() -> None:
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
    with open(username + ".json", "w") as file:
        json.dump(
            {
                "username": username,
                "email": email,
                "password": password,
            },
            file,
            indent=4,
        )
    print("\033[32mUser created successfully!\033[0m")

# function to read user data from .json file and create a User object from it
def readUser(username : str) -> User:
    with open(username + ".json", "r") as file:
        data = json.load(file)
        user = User(data["username"], data["email"], data["password"])
        return user


# function, that asks user to enter username and password, checks if user exists and if password is correct, if so, user is logged in, if not, user is asked to try again
def login() -> None:
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    try:
        user = readUser(username)
        if password == user.password:
            print("\033[32mLogin successful!\033[0m")
            loggedIn(user)
        else:
            print("\033[31mIncorrect password. Please try again.\033[0m")
    # if username is not found, user is asked to try again
    except FileNotFoundError:
        print("\033[31mUser not found. Please try again, or register.\033[0m")


def loggedIn(user : User) -> None:
    while True:
        choice = loggedInMenu()
        match choice:
            case "1":
                print("Search for weather")
                getWeather(user)
            case "2":
                print("Search for news")
                getNews(user)
            case "3":
                changePassword(user)
            case "4":
                print("\033[32mLogged out successfully!\033[0m")
                return
            case "5":
                print("Goodbye!")
                exit()
            case _:
                print("\033[31mInvalid choice. Please try again.\033[0m")
                continue


def loggedInMenu() -> str:
    print("1. Weather")
    print("2. News")
    print("3. Change password")
    print("4. Logout")
    print("5. Exit")
    choice = input("Enter your choice: ")
    return choice


def sendEmail(user : User, message : str) -> None:
    email_sender = EMAIL_SENDER
    email_pass = EMAIL_PASSWORD
    email_receiver = user.email

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = "News+Weather API"
    em.set_content(message)
    context = ssl.create_default_context()

    # with the generated email message, login, authenticate and send email message
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_pass)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


# function to update the user .json file
def updateUser(user):
    with open(user.username + ".json", "w") as file:
        json.dump(
            {
                "username": user.username,
                "email": user.email,
                "password": user.password,
            },
            file,
            indent=4,
        )


# function to change user password when user is logged in
# ask for current password, check if correct, if so, change password
def changePassword(user :User) -> None:
    currentPassword = input("Enter your current password: ")
    if currentPassword == user.password:
        while True:
            password = input(
                "Enter a password. Password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 special character: "
            )
            if user.setPassword(password):
                break
            else:
                continue
        updateUser(user)
        print("\033[32mPassword changed successfully!\033[0m")
    else:
        print("\033[31mIncorrect password. Please try again.\033[0m")


# function to ask user for his username, check if user exists, if so, send email with link to reset password
def resetPassword() -> None:
    username = input("Enter your username: ")
    try:
        user = readUser(username)
        # generate 6 digit code
        code = random.randint(100000, 999999)
        body = f"""Your password reset code is: {code}\n
        Please enter this code in the application to reset your password."""
        sendEmail(user, body)
        print("Password reset code sent to your email address.")
        
        # if code matches, user is asked to enter new password
        while True:
            userCode = input("Enter the code you received: ")
            if userCode == str(code):
                print("\033[32mCode correct!\033[0m")
                while True:
                    password = input(
                        "Enter a password. Password must contain at least 1 number, 1 uppercase, 1 lowercase and 1 special character: "
                    )
                    if user.setPassword(password):
                        break
                    else:
                        continue
                updateUser(user)
                print("\033[32mPassword changed successfully!\033[0m")
            else:
                print("\033[31mCode incorrect. Please try again.\033[0m")
                continue

    except FileNotFoundError:
        print("\033[31mUser not found. Please try again, or register.\033[0m")


# menu function to manage options to user (login, register, exit)
def menu() -> str:
    print("1. Login")
    print("2. Register")
    print("3. Reset password")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice


def main() -> None:
    print("Welcome to the News API!")
    while True:
        # menu fuctionality with case-match to call functions
        print("Please select an option:")
        choice = menu()
        match choice:
            case "1":
                login()
            case "2":
                createUser()
            case "3":
                resetPassword()
            case "4":
                print("Goodbye!")
                exit()
            case _:
                print("\033[31mInvalid choice. Please try again.\033[0m")
                continue


if __name__ == "__main__":
    main()

"""
print("\033[31mThis is red font.\033[0m")
print("\033[32mThis is green font.\033[0m")
print("\033[33mThis is yellow font.\033[0m")
print("\033[34mThis is blue font.\033[0m")


ideas if there is time:
- add email changing functionality (same way with 6 digit code as password reset)
"""
