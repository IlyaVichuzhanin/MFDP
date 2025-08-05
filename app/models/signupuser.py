

class SignUpUser:
    def __init__(self, email:str, password:str):
        self.email=email
        self.password=password

    
class Config:
    """ Model configuration"""
    validate_assignment=True
    arbitrary_types_allowed=True