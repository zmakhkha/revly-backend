import csv
from datetime import datetime
from database import SessionLocal, engine
from models import Base, Chain, User, Vendor, UsersVendors

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Insert Chains
with open("chains.csv", newline="") as f:
    reader = csv.DictReader(f, delimiter=",")
    print("Inserting chains...")
    print(reader.fieldnames)
    for row in reader:
        print(row) 
        db.add(Chain(
            chain_id=int(row['chain_id']),
            name=row["chain_name"],
            created_at=datetime.now()
        ))

# Insert Users
with open("users.csv", newline="") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        db.add(User(
            user_id=int(row["user_id"]),
            display_name=row["display_name"],
            email=row["email"],
            is_active=row["is_active"].upper() == "TRUE",
            created_at=datetime.now()
        ))

# Insert Vendors
with open("vendors.csv", newline="") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        db.add(Vendor(
            vendor_id=int(row["vendor_id"]),
            name=row["vendor_name"],
            chain_id=int(row["chain_id"]),
            longitude=float(row["longitude"]),
            latitude=float(row["latitude"]),
            created_at=datetime.now()
        ))

# Insert users_vendors
with open("users_vendors.csv", newline="") as f:
    reader = csv.DictReader(f, delimiter=",")
    for row in reader:
        db.add(UsersVendors(
            user_id=int(row["user_id"]),
            vendor_id=int(row["vendor_id"]),
            display_name=row["display_name"],
            is_enabled=int(row["is_enabled"]),
            created_at=datetime.now()
        ))

db.commit()
db.close()
