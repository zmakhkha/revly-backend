from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_session, create_db_and_tables
from models import User, Vendor, Chain, UsersVendors
from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime

# Create DB tables
create_db_and_tables()

server = FastAPI()

# --- Pydantic Schemas --- #

class VendorOut(BaseModel):
    vendor_id: int
    name: str
    coordinates: str  # latitude + longitude as string
    chain_id: Optional[int]
    chain_name: Optional[str]
    created_at: datetime


class VendorTag(BaseModel):
    vendor_id: int
    display_name: str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    user_id: int
    email: str
    display_name: str
    is_active: bool
    created_at: datetime
    vendors: List[VendorTag]

    class Config:
        from_attributes = True



# --- Routes --- #

@server.get("/vendors", response_model=List[VendorOut])
def read_vendors(db: Session = Depends(get_session)):
    results = db.query(
        Vendor,
        Chain.name.label("chain_name")
    ).outerjoin(Chain, Vendor.chain_id == Chain.chain_id).all()

    vendors = []
    for vendor, chain_name in results:
        vendors.append(VendorOut(
            vendor_id=vendor.vendor_id,
            name=vendor.name,
            coordinates=f"{vendor.latitude},{vendor.longitude}",
            chain_id=vendor.chain_id,
            chain_name=chain_name,
            created_at=vendor.created_at
        ))

    return vendors


@server.get("/users", response_model=List[UserOut])
def read_users(db: Session = Depends(get_session)):
    users = db.query(User).all()
    output = []

    for user in users:
        # Fetch vendor tags for this user
        user_vendor_links = db.query(UsersVendors).filter_by(user_id=user.user_id).all()

        vendor_tags = [
            VendorTag(vendor_id=link.vendor_id, display_name=link.display_name)
            for link in user_vendor_links
        ]

        output.append(UserOut(
            user_id=user.user_id,
            email=user.email,
            display_name=user.display_name,
            is_active=user.is_active,
            created_at=user.created_at,
            vendors=vendor_tags
        ))

    return output
