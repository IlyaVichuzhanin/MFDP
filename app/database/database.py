from sqlmodel import SQLModel, Session, create_engine
from database.config import get_settings
from models.user import User
from models.admin import Admin
import uuid
from auth.hash_password import HashPassword
from services.crud.user import create_user
from services.crud.admin import create_admin



engine = create_engine(url=get_settings().DATABASE_URL_psycopg, echo=True,pool_size=5, max_overflow=10)
hash_password = HashPassword() 

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        test_user_1_id=uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6")
        hashed_password1=hash_password.create_hash("123")
        test_user_1 = User(email="Bob", hashed_password=hashed_password1, id=test_user_1_id)
        create_user(test_user_1,session)
        test_user_2_id=uuid.UUID("45def698-96b5-47f6-b5a6-b4b4ee0b880c")
        hashed_password2=hash_password.create_hash("123")
        test_user_2 = User(email="Sam", hashed_password=hashed_password2, id=test_user_2_id)
        create_user(test_user_2,session)
        test_user_3_id=uuid.UUID("3870cf70-43df-4d6f-a9ba-b17ed055d99a")
        hashed_password3=hash_password.create_hash("123")
        test_user_3 = User(email="Alice", hashed_password=hashed_password3, id=test_user_3_id)
        create_user(test_user_3,session)
        test_admin_id=uuid.uuid4()
        test_admin_1 = Admin(email="Jack", password="123",id=test_admin_id)
        create_admin(test_admin_1,session)


    

    




