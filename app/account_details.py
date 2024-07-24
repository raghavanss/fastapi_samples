from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from models import Accounts, ClientPartner
from database import get_db
from sqlalchemy.exc import NoResultFound

from schemas import AccountDetailResponse, AccountCreate

from dependencies import verify_google_oauth_token

router = APIRouter()

@router.post("/accounts", response_model=AccountDetailResponse, status_code=201)
async def create_account(account_create: AccountCreate, db: Session = Depends(get_db),
                         token_data: dict = Depends(verify_google_oauth_token)):
    
    try:
        client_partner = db.query(ClientPartner).filter(ClientPartner.name == account_create.client_partner.name).first()
    
        if not client_partner:
            # Create new ClientPartner if not exists
            client_partner = ClientPartner(name=account_create.client_partner.name)
            db.add(client_partner)
            db.commit()
            db.refresh(client_partner)
    
        # Create new Account
        account = Accounts(
            account_name=account_create.account_name,
            region=account_create.region,
            cp_id=client_partner.id 
        )
        db.add(account)
        db.commit()
        db.refresh(account)

        return {
            "account": {
                "id": account.id,
                "account_name": account.account_name,
                "region": account.region,
                "cp_id": account.cp_id
            },
            "client_partner": {
                "id": client_partner.id,
                "name": client_partner.name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail= "Unauthorized Token !!")
   
