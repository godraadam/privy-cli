from typing import Optional

from pydantic import BaseModel


class PrivyContactCreate(BaseModel):
    alias: str
    pubkey: str
    trusted: Optional[bool] = False
    
class PrivyContact(PrivyContactCreate):
    address: str