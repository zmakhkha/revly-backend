
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VendorOut(BaseModel):
    name: str
    longitude: str 
    latitude: str 
    chain_id: Optional[int]
    vendor_id: int
    chain_name: Optional[str]
    created_at: datetime


class VendorTag(BaseModel):
    id: int
    display_name: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    # user_id: int
    email: str
    display_name: str
    is_active: bool
    created_at: datetime
    list_vendors: List[VendorTag]
    
    class Config:
        orm_mode = True
