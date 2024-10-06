from fastapi import APIRouter, HTTPException, Response
from src.services.gpt_api import get_gpt_response
from src.schemas.gpt import GptDataRequest
from fastapi.responses import JSONResponse
router = APIRouter(prefix="/ask_gpt", tags=["GPT"])

@router.post("/", response_class=Response)
def fetch_gpt_response(request: GptDataRequest):
    try:
        response = get_gpt_response(request.question)

        return JSONResponse(content={"response": response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
