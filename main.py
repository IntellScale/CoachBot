
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1HpdMJcKKLzGparmo0cfUw_4Dw-BC2VepAtDD0XyxdUE"  # "1B1myehohvJ5-GpnbtvS_h1pavoi-kQyaGNlwNGjAnGc"

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())

    
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        write_data(sheet)


    except HttpError as e:
        print(e)

def read_data(sheet):
    
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:C3").execute()
    values = result.get("values", [])


    
    for row in values:
        print(row)

def write_data(sheet):
        num_rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:A").execute()
        num_rows = len(num_rows.get("values", []))
        
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!A{num_rows+1}", valueInputOption="USER_ENTERED", body={"values": [["Some name"]]}).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!B{num_rows+1}", valueInputOption="USER_ENTERED", body={"values": [["Some phone number"]]}).execute()
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!C{num_rows+1}", valueInputOption="USER_ENTERED", body={"values": [["Some phone value"]]}).execute()

if __name__ == "__main__":
    main()

