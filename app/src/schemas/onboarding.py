from pydantic import BaseModel

class OnboardingRequest(BaseModel):
    phone_number: str
    message_body: str
