import pandas as pd 
from Google_connect import main, read_data
import time
from datetime import datetime, timedelta

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
            if date_validation == True:
                return True 
 
       
def get_report_record(user_email, query_date):
    sheet = main()

    data = read_data(sheet=sheet)
    data_df = pd.DataFrame(data)
    
    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   
    

    users_submitions = data_df[data_df['Email Address'] == user_email]
    for i in users_submitions.values:
            
            record_date = i[0]
           
            submittion_date = record_date.split(' ')[0]
     
            date_validation = in_same_week(query_date, submittion_date)
            if date_validation == True:
                return i 


     
   
#print(get_report_record('n.andrievskiy@gmail.com', "2023-12-10"))
    
    





    


