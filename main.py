
from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from query_support import validate_presence, get_report_record


from write_file import create_report_file
from user_id_extractor import get_chat_id
from telegram_direct import send_file
from files_manipulation import create_word_document, delete_document
from analytics import calculate_stats

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

    

@app.get("/stats-get/{email}/{time_period}/{stat_type}")
def get_user_stats(email: str, time_period: str, stat_type: str):


    # Extract information from google sheets
    stats = calculate_stats(email, time_period, stat_type)
    
    # Check if stats is JSON serializable
    try:
        json_stats = jsonable_encoder(stats)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
    return json_stats

        # aggregate stats 
 
        #Types of stats 
        # 
        # food
        # measurments
        # positive_state
        # world_feeling
        # spiritual_work
        # full

             
             







    

