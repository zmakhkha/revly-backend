from main import server
from sqlalchemy.orm import Session
from typing import List
from db_config import get_session
from fastapi import Depends
from db_models import Vendor, Chain, User, UsersVendors
from schemas import UserOut, VendorTag, VendorOut

@server.get('/vendors')
def get_vendors(db:Session = Depends(get_session)):
	vendors = db.query(
		Vendor.name.label("vendor_name"),
		Vendor.longitude,
		Vendor.latitude,
		Vendor.chain_id,
		Chain.name.label("chain_name"),
		Vendor.created_at
	).join(
		Chain, Vendor.chain_id == Chain.chain_id
	).all()
	
	results = [VendorOut(
		name= v.vendor_name,
		longitude= v.longitude,
		latitude= v.latitude,
		chain_id= v.chain_id,
		chain_name= v.chain_name,
		created_at= v.created_at
	) for v in vendors]
	return results

@server.get("/users")
def get_users(db:Session= Depends(get_session)):
	results = []
	users = db.query(User
	).all()
	for user in users:
		list_vendors_per_user = db.query(UsersVendors).filter_by(user_id=user.user_id)

		vendors = [VendorTag(
			id= v.vendor_id,
			display_name= v.display_name,
		) for v in list_vendors_per_user]
		
		results.append(UserOut(
			email= user.email,
			display_name= user.display_name,
			is_active= user.is_active,
			created_at= user.created_at,
			list_vendors= vendors
		))
	return results