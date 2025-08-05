from typing import List
from typing import Optional
 
from fastapi import Request
 
class UserSignInForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.email: Optional[str] = None
        self.password: Optional[str] = None
 
    async def load_data(self):
        form = await self.request.form()
        self.email = form.get("email")
        self.password = form.get("password")
