from sqlmodel import SQLModel, Field
from typing import Optional
import uuid



class Admin(SQLModel, table=True):
    __tablename__='admins'
    id: Optional[uuid.UUID] = Field(primary_key=True, unique=True, default_factory=uuid.uuid4)
    email: str = Field(index=True)
    password: str = Field(index=True)






