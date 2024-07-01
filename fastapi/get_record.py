import json
from fastapi import APIRouter
import requests
from database import *

router = APIRouter()

@router.post('/api/v1/validate_token/')
async def validate_token(token: str):
    
    session = Session()
    result = session.query(License).filter(License.token==token).first()
    # result = session.get(Licenses.war_token)

    return {"war_token": f"Ваш рабочий токен: {result.war_token}"}
    