import requests
import os

from query_support import get_report_record

def send_report(file):
    # Replace 'YOUR_TOKEN' with your actual bot token
    bot_token = '6859309312:AAFo5rGYbvh8cgW4cnH8OW2JNqNckmgqWy8'

    # Replace 'USER_ID' with the actual user ID
    user_id = 579467950

    # Replace 'PATH_TO_YOUR_test.csv'

    # Use the sendDocument endpoint to send a file
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # Create a dictionary with the parameters
    params = {
        'chat_id': user_id,
    }

    # Open the file and send it as part of the request
   
    files = {'document': file}
    r = requests.post(url, params=params, files=files)

    # Check the response
    print(r.json())

report = get_report_record("n.andrievskiy@gmail.com", "2023-12-10")
print(report)
send_report(report)