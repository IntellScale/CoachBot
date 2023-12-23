import requests
from datetime import datetime, timedelta
import time
from pytz import timezone
import schedule
import pandas as pd

from Google_connect import main, read_data

# Your Telegram Bot Token
TOKEN = "6859309312:AAFo5rGYbvh8cgW4cnH8OW2JNqNckmgqWy8"
# Your chat message
MESSAGE = "Hello, this is a reminder message!"

# Telegram API base URL
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Kyiv timezone
KYIV_TZ = timezone("Europe/Kiev")

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response.json()

def get_all_ids():
    # Get the Google Sheets API
    sheet = main()

    data = read_data(sheet=sheet, sheet_name="Athlete Names")
    data_df = pd.DataFrame(data)
    
    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]

    # Get all ids
    return data_df["UserId"].values.tolist()

def send_monday_reminders():
    # Get a list of all chat IDs (user IDs)
    chat_ids = get_all_ids()

    # Send the message to all users
    for chat_id in chat_ids:
        try:
            send_message(chat_id, "Доброго ранку!🌞 \nНагадування про тижневий звіт \n\nhttps://docs.google.com/forms/d/1ThR6kOxHfd8Fwt92CiFnXA3nWb7SdLixt8hSFsNUqzw/edit?pli=1")
        except Exception as e:
            print(e)


def send_first_of_month_reminders():
    # Get the current date in Kyiv timezone
    today = datetime.now(KYIV_TZ)

    # Check if today is the first day of the month
    if today.day == 1:
        # Get a list of all chat IDs (user IDs)
        chat_ids = get_all_ids()

        # Send the message to all users
        for chat_id in chat_ids:
            try:
                send_message(chat_id, "Початок місяця! 🌞 \nНагадування про оплату \n\nhttp://secure.wayforpay.com/donate/d550158201eff")
            except Exception as e:
                print(e)

if __name__ == '__main__':
    print("REMINDERS --- WORKING")
    # # Schedule Monday reminders every Monday at 10 AM Kyiv time
    schedule.every().monday.at("10:00").do(send_monday_reminders)

    # Schedule first day of the month reminders at 10 AM Kyiv time
    schedule.every().day.at("10:00").do(send_first_of_month_reminders).tag("first_of_month")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 1 minute to balance responsiveness and efficiency
