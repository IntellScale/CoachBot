
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Api endpoint
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Define the spreasheet we want to access
SPREADSHEET_ID = "1HpdMJcKKLzGparmo0cfUw_4Dw-BC2VepAtDD0XyxdUE"  # "1B1myehohvJ5-GpnbtvS_h1pavoi-kQyaGNlwNGjAnGc"

def main():
    # ==============  AUTHENTICATION TO GOOGLE API ====================

    # Check if credentials exsit
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # Refresh credentials if they have expired
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        # Add credentials
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        
        return sheet


    except HttpError as e:
        print(e)


def read_data(sheet, sheet_name="Form Responses 1"):
    
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A1:BT100").execute()
    values = result.get("values", [])

    return values

def write_data(sheet, sheet_name, data):
    # Get existing data to check for duplicates
    existing_data = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f"{sheet_name}!A:C").execute()
    existing_rows = existing_data.get("values", [])

    # Create a set of existing primary keys for fast lookup
    existing_primary_keys = set(existing_row[0] for existing_row in existing_rows)

    # Prepare new data to be added
    new_rows = []
    for row in data:
        primary_key = row[0]

        # Check if the primary key already exists
        if primary_key not in existing_primary_keys:
            new_rows.append(row)
            existing_primary_keys.add(primary_key)

    if new_rows:
        # Get the number of columns based on the first row of data
        num_columns = len(new_rows[0])

        # Get the next available row
        num_rows = len(existing_rows) + 1

        # Update values for each column
        for col_index in range(num_columns):
            col_values = [row[col_index] if col_index < len(row) else "" for row in new_rows]
            range_str = f"{sheet_name}!{chr(65 + col_index)}{num_rows}"
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=range_str,
                valueInputOption="USER_ENTERED",
                body={"values": [col_values]},
            ).execute()

#if __name__ == "__main__":
  #  main()

