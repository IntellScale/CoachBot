import requests
from docx import Document


# Multi-line string content
multi_line_string = """Hello,
This is a multi-line string.
It will be saved to a Word document and a PDF file.
Have a nice day!
"""

# Save to Word document
doc = Document()
doc.add_paragraph(multi_line_string)
doc.save('output.docx')
print('Word document saved successfully.')

# Replace 'YOUR_TOKEN' with your actual bot token
bot_token = '6859309312:AAFo5rGYbvh8cgW4cnH8OW2JNqNckmgqWy8'

# Replace 'USER_ID' with the actual user ID
user_id = 579467950

# Replace 'PATH_TO_YOUR_FILE' with the actual path to the file you want to send
file_path = 'output.docx'

# Use the sendDocument endpoint to send a file
url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

# Create a dictionary with the parameters
params = {
    'chat_id': user_id,
}

# Open the file and send it as part of the request
with open(file_path, 'rb') as file:
    files = {'document': file}
    r = requests.post(url, params=params, files=files)

# Check the response
print(r.json())
