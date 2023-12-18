import pandas as pd 
from Google_connect import main, read_data
from time_category import is_in_last_two_weeks,is_in_last_month, is_in_last_quarter, is_in_last_year
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

    data = read_data(sheet= sheet)
    

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

    data = read_data(sheet= sheet)
    

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

                
def get_user_submittions_data(user_email) :
    sheet = main()

    data = read_data(sheet= sheet)
    

    data_df = pd.DataFrame(data)
    

    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   
    

    users_submitions = data_df[data_df['Email Address'] == user_email]

    return users_submitions

def filter_submittions_time_category(row , time_frame_category):
     # Possible types
     ## last_two_weeks
        #last_month
        ##last_quarter
        #last_year'''
    # Extract the date 
    date = datetime.strptime(row[0].split(" ")[0], "%m/%d/%Y")


    if time_frame_category == "last_two_weeks":
        return is_in_last_two_weeks(date)
    
    if time_frame_category == "last_month":
        return is_in_last_month(date)
    
    if time_frame_category == "last_quarter": 
        return is_in_last_quarter(date)
    
    if time_frame_category == "last_year":
        return is_in_last_year(date)
         
     
        





    


    
