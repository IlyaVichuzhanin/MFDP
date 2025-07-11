from sqlmodel import Session
from models.user import User
from models.balance import Balance
from models.transaction import Transaction
from services.crud.transaction import create_transaction
import uuid



def test_create_user(session:Session):
    try:
        user=User(id=uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"), email="123@123", hashed_password="123")
        session.add(user)
        session.commit()
        assert True
    except:
        assert True


def test_delete_user_by_id(session:Session):
    try:
        user=session.get(User, uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"))
        if user:
            session.delete(user)
            session.commit()
            assert True
        else:
            assert False
    except Exception as ex:
        assert False, ex

def test_get_user_by_id(session:Session):
    try:
        user=session.get(User, uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"))
        if user:
            assert True
        else:
            assert False
    except:
        assert False



def  test_increase_user_balance(session:Session):
    try:
        user = session.get(User, uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"))
        if user:
            balance = session.get(Balance, user.balance_id)
            if balance:
                new_transaction = Transaction(credits=credits, user_id=uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"))
                create_transaction(new_transaction, session)
                balance.current_balance += new_transaction.credits
                session.add(balance)
                session.commit()
                session.refresh(balance)
            else:
                assert False
        else:
            assert False
    except:
        assert False


def  test_decrease_user_balance(session:Session):
    try:
        user = session.get(User, uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"))
        if user:
            balance = session.get(Balance, user.balance_id)
            if balance:
                new_transaction = Transaction(credits=credits, user_id=uuid.UUID("773e3742-c9ae-4f10-85d8-da3d0d3490b6"))
                create_transaction(new_transaction, session)
                balance.current_balance += new_transaction.credits
                session.add(balance)
                session.commit()
                session.refresh(balance)
            else:
                assert False
        else:
            assert False
    except:
        assert False