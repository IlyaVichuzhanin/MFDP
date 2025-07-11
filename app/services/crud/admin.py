from models.admin import Admin
from typing import List, Optional
import uuid


def get_all_admins(session)->List[Admin]:
    return session.query(Admin).all()

def get_admin_by_id(id:uuid.UUID, session) -> Optional[Admin]:
    admin=session.get(Admin, id)
    if admin:
        return admin
    return None

def get_user_by_email(email:str, session) -> Optional[Admin]:
    admin = session.query(Admin).filter(Admin.email==email).first()
    if admin:
        return admin
    return None


def create_admin(new_admin: Admin, session) -> None:
    session.add(new_admin)
    session.commit()
    session.refresh(new_admin)

def delete_admin_by_id(id:uuid.UUID, session) -> None:
    admin = session.get(Admin, id)
    if admin:
        session.delete[admin]
        session.commit()
        return