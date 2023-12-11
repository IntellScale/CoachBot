
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from query_support import validate_presence, get_report_record

from send_file import send_report
from write_file import create_report_file
from user_id_extractor import get_chat_id


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
    google_sheets_data = get_report_record(email, date)
    report = create_report_file(google_sheets_data)

    chat_id = get_chat_id(user_name)
    
    send_report(report, chat_id)
    

