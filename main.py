from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Creating an instance of fast api
app = FastAPI()

class Item(BaseModel):
    user_id : int
    date: str



items ={
    1: Item(user_id = 123, date = "25.12.2023", other_stats = "here we can put what we want")
}

@app.get("/reports/{record_id}/{date}")
def quesry_user_reports(item_id : int, date:str ):
    print(items.values())
    
    if item_id not in items :
        raise HTTPException(status_code= 404, detail = f"The user with {item_id} does not exist in the system")
        
    return {"item": items[item_id]}
