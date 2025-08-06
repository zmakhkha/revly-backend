from datetime import datetime
from db_models import Vendor, Chain, User, UsersVendors
from db_config import get_session
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from main import server
from sqlalchemy.orm import Session
from schemas import UserOut, VendorTag, VendorOut, UserIn

@server.get('/vendors')
def get_vendors(db: Session = Depends(get_session)):
    vendors = db.query(
        Vendor.vendor_id,                        
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
        vendor_id=v.vendor_id,                     
        vendor_name=v.vendor_name,
        longitude=v.longitude,
        latitude=v.latitude,
        chain_id=v.chain_id,
        chain_name=v.chain_name,
        created_at=v.created_at
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
			vendor_id= v.vendor_id,
			vendor_name= v.display_name,
		) for v in list_vendors_per_user]
		
		results.append(UserOut(
			user_id=user.user_id,
			email= user.email,
			display_name= user.display_name,
			is_active= user.is_active,
			created_at= user.created_at,
			vendors= vendors
		))
	return results

@server.post("/users")
def post_user(user: UserIn, db:Session = Depends(get_session)):
	db_user = User(
		email = user.email,
		display_name = user.display_name,
		created_at = datetime.now(),
		is_active = False
	)
	db.add(db_user)
	db.commit()
	return user

@server.put("/users/{id}")
def modify_user(id:int, user:UserIn, db:Session=Depends(get_session)):
	selected_user = db.query(User).filter_by(user_id=id).first()
	if selected_user is None:
		raise HTTPException(status_code=404, detail="USer Not Found !!")
	
	# selected_user.email = user.email
	# selected_user.display_name = user.display_name
	selected_user.is_active = user.is_active
	db.commit()
	db.refresh(selected_user)

	return {"message": "User updated successfully"}

@server.delete("/users/{id}")
def modify_user(id:int, db:Session=Depends(get_session)):
	selected_user = db.query(User).filter_by(user_id=id).first()
	if selected_user is None:
		raise HTTPException(status_code=404, detail="USer Not Found !!")
	db.delete(selected_user)
	db.commit()

	return JSONResponse( status_code=200, content={"details": "User deleted successfully!"}
    )