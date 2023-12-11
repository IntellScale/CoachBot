
from fastapi import FastAPI

from query_support import validate_presence, get_report_record


from write_file import create_report_file
from user_id_extractor import get_chat_id
from send_file import send_report
from files_manipulation import create_word_document, delete_document


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
    report_file_path = "output_documenet.docx"

    # Extract information from google sheets
    google_sheets_data = get_report_record(email, date)
    #Create report text using the template 
    report = create_report_file(google_sheets_data)


   
    create_word_document(report, report_file_path)

    # Extract chat id
    chat_id = get_chat_id(user_name)
   
    send_report(report_file_path,chat_id)
    delete_document(report_file_path)




    

