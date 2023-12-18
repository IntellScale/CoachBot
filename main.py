
from fastapi import FastAPI

from query_support import validate_presence, get_report_record, get_user_submittions_data, filter_submittions_time_category


from write_file import create_report_file
from user_id_extractor import get_chat_id
from telegram_direct import send_file
from files_manipulation import create_word_document, delete_document
from analytics import calculate_stats, build_graph

# Creating an instance of fast api
app = FastAPI()

@app.get("/reports-check/{email}/{date}")
def query_user_reporst(email: str , date:str) -> bool:
    validation_result = validate_presence(email, date)
    print(validation_result)
    print(email, date)
    return validation_result

@app.get("/reports-get/{user_name}/{email}/{date}")
def get_user_report(user_name: str,email: str, date : str):
    try:
        report_file_path = "output_documenet.docx"

        # Extract information from google sheets
        google_sheets_data = get_report_record(email, date)
        #Create report text using the template 
        report = create_report_file(google_sheets_data)

        # Creating word file
        create_word_document(report, report_file_path)

        # Extract chat id
        chat_id = get_chat_id(user_name)
        
        # Sening report
        send_file(report_file_path,chat_id)

        # Delete report
        delete_document(report_file_path)

        return {"successful": True}
    except: {"successful": False}

@app.get("/stats-get/user_name={user_name}/email={email}/date_type={date_type}/stat_type={stat_type}")
def get_user_stats(user_name: str,email: str, date_type : str, stat_type: str):
    # Extract information from google sheets
        google_sheets_data = get_user_submittions_data(user_email=email)

        # Retrive the information for the correct time frame 
        date_filtered_submittions = google_sheets_data[google_sheets_data.apply(filter_submittions_time_category, axis = 1, time_frame_category = date_type )]

        # aggregate stats 

        #Types of stats 
        # 
        # food
        # measurments
        # positive_state
        # word_feeling
        # spiritual_work
        # full

    
        if stat_type == "food": 
             
             
             







    

