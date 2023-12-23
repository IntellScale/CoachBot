from pydantic import BaseModel

class Feedback(BaseModel):
    username: str
    feedback: str