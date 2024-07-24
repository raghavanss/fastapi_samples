from sqlalchemy.orm import (declarative_base, 
                            sessionmaker, 
                            Session,
                              relationship
                              )

from sqlalchemy import (Column,
                         String,
                           Integer,
                             create_engine,
                             ForeignKey)

from faker import Faker


DATABASE_URL = "sqlite:///./test1.db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

fk = Faker()

#User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    addresses = relationship("Address", back_populates="user")


#Address model
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index= True)
    user_id = Column(Integer, ForeignKey('users.id'))

    address = Column(String, index= True)

    user = relationship("User", back_populates="addresses")



Base.metadata.create_all(bind= engine)


def insert_sample_data(db: Session):
    user1 = User(name = fk.first_name())
    user2 = User(name = fk.first_name())

    address1  = Address( address = fk.address(), user=user1)
    address2  = Address( address = fk.address(), user=user2)


    db.add(user1)
    db.add(user2)
    db.add(address1)
    db.add(address2)
    db.commit()



db = SessionLocal()
insert_sample_data(db)
db.close()
