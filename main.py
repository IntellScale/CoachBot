
from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from query_support import validate_presence, get_report_record

from send_file import send_report


# Creating an instance of fast api
app = FastAPI()

@app.get("/reports-check/{email}/{date}")
def query_user_reporst(email: str , date:str) -> bool:
    validation_result = validate_presence(email, date)
    print(validation_result)
    print(email, date)
    return validation_result

@app.get("/reports-get/{email}/{date}")
def get_user_report(email: str, date : str):
    report = get_report_record(email, date)
    send_report(report)
    

