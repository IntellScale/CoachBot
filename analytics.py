import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime, timedelta

from Google_connect import main, read_data

def calculate_stats(user_email, time_period, stat_field, plots_folder="plots"):
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
                # Generate plot for the singular field
                plot_file_path = os.path.join(plots_folder, f'{field.replace(" ", "-")}_plot.png')
                generate_plot(time_filtered_data['Timestamp'], numeric_values, field, plot_file_path, time_period)

                    
                result_dict[field] = {
                    'min': float(numeric_values.min()),
                    'max': float(numeric_values.max()),
                    'avg': float(numeric_values.mean()),
                    "plot_path": plot_file_path
                }

            except ValueError as e:
                print(e)
                result_dict[field] = {
                    'min': None,
                    'max': None,
                    'avg': None,
                    "plot_path": None
                }


    elif stat_field == "measurements":
        fields = ["Вага", "Плечі", "Груди", "Рука права", "Рука ліва", "Талія", "Стегна", "Стегно праве", "Стегно ліве"]
        for field in fields:
            try:
                numeric_values = pd.to_numeric(time_filtered_data[field])
                # Generate plot for the singular field
                plot_file_path = os.path.join(plots_folder, f'{field.replace(" ", "-")}_plot.png')
                generate_plot(time_filtered_data['Timestamp'], numeric_values, field, plot_file_path, time_period)
                    
                result_dict[field] = {
                    'min': float(numeric_values.min()),
                    'max': float(numeric_values.max()),
                    'avg': float(numeric_values.mean()),
                    'plot_path': plot_file_path
                }

            except ValueError as e:
                print(e)
                result_dict[field] = {
                    'min': None,
                    'max': None,
                    'avg': None,
                    'plot_path': None
                }

    elif stat_field == "all":
            # Include all stat fields (food, measurements, positive_state, field_4, field_5)
            all_fields = ["food", "measurements", "Щирість позитивного стану", "Відчуття дзеркала світу", "Робота з душею"]
            for field in all_fields:
                if field == "food" or field == "measurements":
                    # Include individual features for 'food' and 'measurements'
                    sub_fields = ["Білків", "Жиров", "Вуглеводів", "ККАЛ"] if field == "food" else ["Вага", "Плечі", "Груди", "Рука права", "Рука ліва", "Талія", "Стегна", "Стегно праве", "Стегно ліве"]
                    for sub_field in sub_fields:
                        try:
                            numeric_values = pd.to_numeric(time_filtered_data[sub_field])
                            # Generate plot for the singular field
                            plot_file_path = os.path.join(plots_folder, f'{sub_field.replace(" ", "-")}_plot.png')
                            generate_plot(time_filtered_data['Timestamp'], numeric_values, sub_field, plot_file_path, time_period)

                            result_dict[sub_field] = {
                                'min': float(numeric_values.min()),
                                'max': float(numeric_values.max()),
                                'avg': float(numeric_values.mean()),
                                'plot_path': plot_file_path
                            }
                        except ValueError as e:
                            result_dict[sub_field] = {
                                'min': None,
                                'max': None,
                                'avg': None,
                                'plot_path': None
                            }
                else:
                    # Include single columns for other stat fields
                    try:
                        numeric_values = pd.to_numeric(time_filtered_data[field])
                        # Generate plot for the singular field
                        plot_file_path = os.path.join(plots_folder, f'{field.replace(" ", "-")}_plot.png')
                        generate_plot(time_filtered_data['Timestamp'], numeric_values, field, plot_file_path, time_period)
                    
                        result_dict[field] = {
                            'min': float(numeric_values.min()),
                            'max': float(numeric_values.max()),
                            'avg': float(numeric_values.mean()),
                            'plot_path': plot_file_path
                        }
                    except ValueError as e:
                        result_dict[field] = {
                            'min': None,
                            'max': None,
                            'avg': None,
                            'plot_path': None
                        }


    else:
        try:
            numeric_values = pd.to_numeric(time_filtered_data[stat_field])
            # Generate plot for the singular field
            plot_file_path = os.path.join(plots_folder, f'{stat_field.replace(" ", "-")}_plot.png')
            generate_plot(time_filtered_data['Timestamp'], numeric_values, stat_field, plot_file_path, time_period)
            
            result_dict[stat_field] = {
                'min': float(numeric_values.min()),
                'max': float(numeric_values.max()),
                'avg': float(numeric_values.mean()),
                "plot_path": plot_file_path
            }

        except ValueError as e:
            print(e)
            result_dict[stat_field] = {
                'min': None,
                'max': None,
                'avg': None
            }

    return result_dict

def generate_plot(timestamps, numeric_values, stat_field, plot_file_path, period_type):
    # Convert timestamps to datetime objects
    datetime_timestamps = [pd.to_datetime(ts).to_pydatetime() for ts in timestamps]

    # Create the plot using Matplotlib
    plt.plot(datetime_timestamps, numeric_values, label=stat_field)

    # Customize the x-axis based on the period type
    if period_type == 'last_2_weeks':
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    elif period_type == 'last_month':
        plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    elif period_type == 'last_quarter':
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonthday=-1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    elif period_type == 'last_year':
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    plt.xlabel('Time')
    plt.ylabel(stat_field)
    plt.title(f'{stat_field} Progression Over Time')
    plt.legend()

    # Save the plot to the specified file path
    plt.savefig(plot_file_path)
    plt.close()

