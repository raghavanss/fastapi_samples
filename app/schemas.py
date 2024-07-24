
from pydantic import BaseModel

class AccountResponse(BaseModel):
    id: int
    account_name: str
    region: str
    cp_id:int

class ClientPartnerResponse(BaseModel):
    id: int
    name: str

class AccountDetailResponse(BaseModel):
    account: AccountResponse
    client_partner: ClientPartnerResponse

class ClientPartnerCreate(BaseModel):
    name: str

class AccountCreate(BaseModel):
    account_name: str
    region: str
    client_partner: ClientPartnerCreate

