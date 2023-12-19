import requests
import os

from query_support import get_report_record

class TelegramMessanger:
    def __init__(self, bot_token):
        self.bot_token = bot_token

    def send_file(self, file_path: str, chat_id: int):
        # Replace 'PATH_TO_YOUR_test.csv'

        # Use the sendDocument endpoint to send a file
        url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"

        # Create a dictionary with the parameters
        params = {
            'chat_id': chat_id,
        }

        # Open the file and send it as part of the request
        with open(file_path, 'rb') as file:
            files = {'document': file}
            r = requests.post(url, params=params, files=files)

        # Check the response
        print(r.json())


    def send_message(self, message, chat_id: int):
        # Use the sendDocument endpoint to send a file
        url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"

        # Create a dictionary with the parameters
        params = {
            'chat_id': chat_id,
        }

        # Open the file and send it as part of the request
    
        files = {'message': message}
        r = requests.post(url, params=params, files=files)

        # Check the response
        print(r.json())