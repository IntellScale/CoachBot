import pandas as pd 
import pytz
from datetime import datetime, timedelta
from Google_connect import main, read_data, write_data
from user_id_extractor import get_chat_id

def add_user_to_sheet(email, full_name, user_name):
    chat_id = get_chat_id(user_name)

    data = [[email, full_name, user_name, chat_id]] # Needs to be a double list
    sheet = main()

    write_data(sheet, "Athlete Names", data)

def convert_date(date_str):
    if date_str.lower() == "today":
        today_date = datetime.now().strftime("%Y-%m-%d")
        return today_date
    else:
        try:
            # Try to parse as dd.mm.yyyy
            input_date = datetime.strptime(date_str, "%d.%m.%Y").strftime("%Y-%m-%d")
            return input_date
        except ValueError:
            # If parsing fails, return the original input
            return date_str   

def in_same_week(date1, date2):
    # Convert input strings to datetime objects
    date1 = datetime.strptime(date1, "%Y-%m-%d")
    date2 = datetime.strptime(date2, "%m/%d/%Y")

    # Calculate the Monday of the week for each date
    monday1 = date1 - timedelta(days=date1.weekday())
    monday2 = date2 - timedelta(days=date2.weekday())
 
    # Check if both dates are in the same week
    return monday1 == monday2

def validate_presence(user_email, validation_date):
    sheet = main()
    data = read_data(sheet=sheet)
    data_df = pd.DataFrame(data)

    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   
    

    users_submitions = data_df[data_df['Email Address'] == user_email][["Timestamp"]]
    for i in users_submitions.values:
        date = i[0].split(' ')[0]
        date_validation = in_same_week(validation_date, date)
        if date_validation is True:
            return True
    
    return False

def get_report_record(user_email, query_date):
    query_date = convert_date(query_date)

    sheet = main()

    data = read_data(sheet=sheet)
    data_df = pd.DataFrame(data)
    
    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   
    

    users_submitions = data_df[data_df['Email Address'] == user_email]
    for i in users_submitions.values:
            
            record_date = i[0]
           
            submition_date = record_date.split(' ')[0]
     
            date_validation = in_same_week(query_date, submition_date)
            if date_validation == True:
                return i 
            else:
                return False

def get_all_athletes():
    sheet = main()

    data = read_data(sheet=sheet, sheet_name="Athlete Names")
    data_df = pd.DataFrame(data)
    
    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   

    all_athletes = data_df["Name"].unique()

    message = ""
    for i, name in enumerate(all_athletes):
        message += f"{i+1}. {name} \n"
    
    return message

def get_indexed_athlete(index):
    sheet = main()

    data = read_data(sheet=sheet, sheet_name="Athlete Names")
    data_df = pd.DataFrame(data)
    
    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   

    all_athletes = data_df["Email"].unique()

    return all_athletes[index-1]

def add_feedback_to_sheet(username: str, feedback: str):
    # Get the current date and time in ISO format
    kyiv_timezone = pytz.timezone("Europe/Kiev")
    timestamp = datetime.now(kyiv_timezone).isoformat()
    data = [[timestamp, username, feedback]]

    sheet = main()
    write_data(sheet, "Feedback", data)
     
    
    





    


