from fastapi import Security, HTTPException
import requests
from starlette.config import Config

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
config = Config('.env')
GOOGLE_CLIENT_ID = config.get('GOOGLE_CLIENT_ID')

async def verify_google_oauth_token(token: str = Security(oauth2_scheme)):
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid Google OAuth token")
    token_info = response.json()
    if 'aud' not in token_info or token_info['aud'] != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=400, detail="Invalid Google OAuth token")
    return token_info