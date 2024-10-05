from pydantic import BaseModel

class GptDataRequest(BaseModel):
    question: str 


