import datetime
from sqlmodel import SQLModel, Field, Relationship, LargeBinary
from typing import Optional
from sqlalchemy import Column
from typing import TYPE_CHECKING, Optional
from PIL import Image
import uuid
if TYPE_CHECKING:
    from models.user import User
    from models.response import Response

class Request(SQLModel, table=True):
    __tablename__="requests"
    id: Optional[uuid.UUID] = Field(primary_key=True, unique=True, default_factory=uuid.uuid4)
    image: Optional[str] = Field(index=True)
    date_time: str = Field(index=True, default=datetime.datetime.now())
    user_id: Optional[uuid.UUID] = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(
         back_populates="requests"
    )
    response: Optional["Response"] = Relationship(back_populates="request", sa_relationship_kwargs={'uselist': False})



class Config:
    """ Model configuration"""
    validate_assignment=True
    arbitrary_types_allowed=True

class CreateRequest(SQLModel, table=False):

    image_path: str  = Field(..., index=True)
    














# import datetime
# from tkinter import Image


# class Request:

#     def __init__(self, request:Image, requestDateTime:datetime):
#         self.__request = request
#         self.__requestDateTime = requestDateTime
    
#     @property
#     def request(self):
#         return self.__request
    
#     @property
#     def requestDateTime(self):
#         return self.__requestDateTime