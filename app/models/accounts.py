
from database import Base

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

class Accounts(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String(50), unique=True, index=True)
    region = Column(String, index= True)
    cp_id = Column(Integer, ForeignKey('client_partner.id'))

    client_partner_id =  relationship("ClientPartner", back_populates="accounts")

    
class ClientPartner(Base):
    __tablename__ = "client_partner"
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String(100), index=True)

    accounts = relationship("Accounts", back_populates="client_partner_id")

