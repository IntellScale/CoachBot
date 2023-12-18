import pandas as pd 
from Google_connect import main, read_data
import time
from datetime import datetime, timedelta

def calculate_stats(user_email, time_period, stat_field):
    sheet = main()

    data = read_data(sheet=sheet)
    data_df = pd.DataFrame(data)
    
    data_df.columns = data_df.iloc[0]
    data_df = data_df[1:]   
    data_df['Timestamp'] = pd.to_datetime(data_df['Timestamp'])
    
    # Filter data by user_email
    user_data = data_df[data_df['Email Address'] == user_email]

    # Calculate the start date based on the selected time_period
    if time_period == 'last_2_weeks':
        start_date = datetime.now() - timedelta(weeks=2)
    elif time_period == 'last_month':
        start_date = datetime.now() - timedelta(weeks=4)
    elif time_period == 'last_quarter':
        start_date = datetime.now() - timedelta(weeks=13)
    elif time_period == 'last_year':
        start_date = datetime.now() - timedelta(weeks=52)
    else:
        raise ValueError("Invalid time_period")

    # Filter data by the selected time_period
    time_filtered_data = user_data[user_data['Timestamp'] >= start_date]
# Calculate statistics
    result_dict = {}

    if stat_field == "food":
        fields = ["Білків", "Жиров", "Вуглеводів", "ККАЛ"]
        for field in fields:
            try:
                numeric_values = pd.to_numeric(time_filtered_data[field])
                    
                result_dict[field] = {
                    'avg': float(numeric_values.mean()),
                    'min': float(numeric_values.min()),
                    'max': float(numeric_values.max())
                }

            except ValueError as e:
                print(e)
                result_dict[field] = {
                    'avg': None,
                    'min': None,
                    'max': None
                }


    elif stat_field == "measurements":
        fields = ["Вага", "Плечі", "Груди", "Рука права", "Рука ліва", "Талія", "Стегна", "Стегно праве", "Стегно ліве"]
        for field in fields:
            try:
                numeric_values = pd.to_numeric(time_filtered_data[field])
                    
                result_dict[field] = {
                    'avg': float(numeric_values.mean()),
                    'min': float(numeric_values.min()),
                    'max': float(numeric_values.max())
                }

            except ValueError as e:
                print(e)
                result_dict[field] = {
                    'avg': None,
                    'min': None,
                    'max': None
                }

    else:
        try:
            numeric_values = pd.to_numeric(time_filtered_data[stat_field])
                
            result_dict[stat_field] = {
                'avg': float(numeric_values.mean()),
                'min': float(numeric_values.min()),
                'max': float(numeric_values.max())
            }

        except ValueError as e:
            print(e)
            result_dict[stat_field] = {
                'avg': None,
                'min': None,
                'max': None
            }

    return result_dict


# stats = calculate_stats("n.andrievskiy@gmail.com", "last_month", "food")
# print(stats)
