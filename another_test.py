import requests 

bot_token = '6859309312:AAFo5rGYbvh8cgW4cnH8OW2JNqNckmgqWy8'

# Replace 'USERNAME_TO_FIND' with the username you want to find
username_to_find = 'NAndriievskyi'

# Use the getUpdates endpoint to get the latest updates
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
response = requests.get(url)
data = response.json()

# Check if the response is successful
if data['ok']:
    # Iterate through the updates
    for update in data['result']:
        # Check if the update contains a message and has the specified username
        if 'message' in update and 'from' in update['message'] and 'username' in update['message']['from']:
            if update['message']['from']['username'] == username_to_find:
                # Extract the chat ID
                chat_id = update['message']['chat']['id']
                print(f"Chat ID for username '{username_to_find}': {chat_id}")
                break
    else:
        print(f"Username '{username_to_find}' not found in the updates.")
else:
    print(f"Error: {data['description']}")
