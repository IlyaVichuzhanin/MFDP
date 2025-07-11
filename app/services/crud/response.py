from models.response import Response
from typing import List, Optional
from services.crud import request as RequestService
import uuid
from sqlmodel import Session


def get_all_responses(session:Session)->List["Response"]:
    return session.query(Response).all()

def get_responce_by_id(id:uuid.UUID, session) -> Optional["Response"]:
    responce=session.get(Response, id)
    if responce:
        return responce
    return None

def get_user_responses(user_id:uuid.UUID, session:Session) -> Optional[List["Response"]]:
    return session.query(Response).all()


def create_response(new_response: "Response", session) -> None:
    session.add(new_response)
    session.commit()
    session.refresh(new_response)

def delete_response_by_id(id:uuid.UUID, session) -> None:
    response = session.get(Response, id)
    if response:
        session.delete[response]
        session.commit()
        return
    

def get_response_by_request_id(request_id:uuid.UUID, session:Session) -> Optional["Response"]:
    response = session.query(Response).filter(Response.request_id==request_id).first()
    if response:
        return response
    else:
        return None

