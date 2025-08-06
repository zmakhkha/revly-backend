from sqlalchemy import Column, Integer, ForeignKey, String, TIMESTAMP, Boolean, Float
from db_config import Base

class User(Base):
	__tablename__ = "user"
	user_id = Column(Integer, primary_key=True)
	display_name = Column(String)
	email = Column(String)
	is_active = Column(Boolean)
	created_at = Column(TIMESTAMP)


class Chain(Base):
	__tablename__ = "chain"
	chain_id = Column(Integer, primary_key=True)
	name = Column(String)
	created_at = Column(TIMESTAMP)

class Vendor(Base):
	__tablename__ = "vendor"
	vendor_id = Column(Integer, primary_key=True)
	name = Column(String)
	chain_id = Column(Integer, ForeignKey("chain.chain_id"))
	longitude = Column(Float)
	latitude = Column(Float)
	created_at = Column(TIMESTAMP)

class UsersVendors(Base):
	__tablename__ = "users_vendors"
	user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
	vendor_id = Column(Integer, ForeignKey("vendor.vendor_id"), primary_key=True)
	display_name = Column(String)
	is_enabled = Column(Boolean)
	created_at = Column(TIMESTAMP)