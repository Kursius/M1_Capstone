import unittest
import os
from unittest.mock import patch
from io import StringIO

# Import functions and classes from the news.py file
from news import User, getWeather, getNews, createUser, readUser, login, loggedIn, changePassword, resetPassword

class TestNewsApp(unittest.TestCase):

    def setUp(self):
        # Set up environment variables for testing
        os.environ["API_WEATHER"] = "your_weather_api_key"
        os.environ["API_NEWS"] = "your_news_api_key"
        os.environ["EMAIL_SENDER"] = "your_email_sender"
        os.environ["EMAIL_PASSWORD"] = "your_email_password"

    def tearDown(self):
        # Clear environment variables after testing
        os.environ["API_WEATHER"] = ""
        os.environ["API_NEWS"] = ""
        os.environ["EMAIL_SENDER"] = ""
        os.environ["EMAIL_PASSWORD"] = ""

    def test_user_creation(self):
        # Test User creation and data validation
        user = User()
        self.assertTrue(user.setUsername("testuser"))
        self.assertTrue(user.setEmail("test@example.com"))
        self.assertTrue(user.setPassword("P@ssw0rd"))
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password, "P@ssw0rd")

    @patch("builtins.input", side_effect=["Technology", "5"])
    def test_get_news(self, mock_input):
        # Test getNews function with mock inputs
        user = User()
        with patch("requests.get") as mock_get:
            mock_get.return_value.json.return_value = {
                "totalResults": 5,
                "articles": [
                    {
                        "title": "News 1",
                        "description": "Description 1",
                        "url": "http://example.com/news1"
                    },
                    {
                        "title": "News 2",
                        "description": "Description 2",
                        "url": "http://example.com/news2"
                    },
                    {
                        "title": "News 3",
                        "description": "Description 3",
                        "url": "http://example.com/news3"
                    },
                    {
                        "title": "News 4",
                        "description": "Description 4",
                        "url": "http://example.com/news4"
                    },
                    {
                        "title": "News 5",
                        "description": "Description 5",
                        "url": "http://example.com/news5"
                    }
                ]
            }
            with patch("news.sendEmail") as mock_send_email:
                getNews(user)
                mock_send_email.assert_called_once()

    @patch("builtins.input", side_effect=["testuser", "P@ssw0rd"])
    def test_login(self, mock_input):
        # Test login function with mock inputs
        user = User("testuser", "test@example.com", "P@ssw0rd")
        with patch("news.readUser") as mock_read_user:
            mock_read_user.return_value = user
            with patch("news.loggedIn") as mock_logged_in:
                login()
                mock_logged_in.assert_called_once()

    @patch("builtins.input", side_effect=["P@ssw0rd", "NewP@ssw0rd"])
    def test_change_password(self, mock_input):
        # Test changePassword function with mock inputs
        user = User("testuser", "test@example.com", "P@ssw0rd")
        with patch("news.updateUser") as mock_update_user:
            changePassword(user)
            mock_update_user.assert_called_once()

    @patch("builtins.input", side_effect=["testuser"])
    def test_reset_password(self, mock_input):
        # Test resetPassword function with mock inputs
        user = User("testuser", "test@example.com", "P@ssw0rd")
        with patch("news.readUser") as mock_read_user:
            mock_read_user.return_value = user
            with patch("news.input", return_value="123456"):
                with patch("news.sendEmail") as mock_send_email:
                    resetPassword()
                    mock_send_email.assert_called_once()

if __name__ == "__main__":
    unittest.main()
