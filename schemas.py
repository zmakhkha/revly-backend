
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VendorOut(BaseModel):
    vendor_id: int
    name: str
    coordinates: str 
    chain_id: Optional[int]
    chain_name: Optional[str]
    created_at: datetime


class VendorTag(BaseModel):
    vendor_id: int
    display_name: str

    class Config:
        from_attributes = True
()
class User(BaseModel):
    user_id: int
    email: str
    display_name: str
    is_active: bool
    created_at: datetime
    vendors: List[VendorTag]

    class Config:
        from_attributes = True