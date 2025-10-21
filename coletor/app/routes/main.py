from fastapi import APIRouter

from app.lib.logger import Logger
from app.lib.custom_response import generate_json_response

log = Logger()
router = APIRouter()

# health
@router.get('/')
async def main():
    return generate_json_response(response_data={'data': {'/': 'OK'}})
