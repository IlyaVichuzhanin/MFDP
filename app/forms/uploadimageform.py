from typing import List
from typing import Optional
from fastapi import Request, UploadFile
 

class UploadImageForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.file: UploadFile = None
 
    async def load_data(self):
        form = await self.request.form()
        self.file = form.get("file")